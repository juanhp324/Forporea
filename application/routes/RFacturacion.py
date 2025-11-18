from flask import request, Blueprint, jsonify, send_file
from datetime import datetime
import pytz
import infrasture.model.MFacturacion as MFacturacion
import domain.VFacturacion as VFacturacion
from domain.VPermisos import requiere_permiso
from infrasture.jwt_utils import token_required, get_current_user
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
import io
from bson import ObjectId

bp = Blueprint('RFacturacion', __name__)

@bp.route('/facturas', methods=['GET'])
@token_required
def get_facturas():
    try:
        facturas_cursor = MFacturacion.getAllFacturas()
        facturas_list = []
        
        for factura in facturas_cursor:
            # Convertir ObjectId en productos
            productos_serializables = []
            for prod in factura.get('productos', []):
                productos_serializables.append({
                    'producto_id': str(prod.get('producto_id')) if prod.get('producto_id') else '',
                    'nombre': prod.get('nombre', ''),
                    'cantidad': prod.get('cantidad', 0),
                    'precio_unitario': prod.get('precio_unitario', 0),
                    'subtotal': prod.get('subtotal', 0)
                })
            
            # Formatear fecha de manera segura
            fecha_str = ''
            try:
                if factura.get('fecha'):
                    fecha_str = factura.get('fecha').strftime('%d/%m/%Y %H:%M')
            except:
                fecha_str = str(factura.get('fecha', ''))
            
            facturas_list.append({
                '_id': str(factura['_id']),
                'cliente': factura.get('cliente', ''),
                'fecha': fecha_str,
                'total': factura.get('total', 0),
                'productos': productos_serializables
            })
        
        return jsonify({"success": True, "facturas": facturas_list})
    except Exception as exc:
        return jsonify({"success": False, "message": str(exc)}), 500

@bp.route('/productos-factura', methods=['GET'])
@token_required
def get_productos_factura():
    try:
        productos_cursor = MFacturacion.getAllProductos()
        productos_list = []
        
        for producto in productos_cursor:
            productos_list.append({
                '_id': str(producto['_id']),
                'nombre': producto.get('nombre', ''),
                'precio': producto.get('precio', 0),
                'stock': producto.get('stock', 0)
            })
        
        return jsonify({"success": True, "productos": productos_list})
    except Exception as exc:
        return jsonify({"success": False, "message": str(exc)}), 500

@bp.route('/facturas', methods=['POST'])
@token_required
@requiere_permiso('facturacion', 'crear')
def create_factura():
    try:
        data = request.get_json(silent=True)
        validator = VFacturacion.createFacturaValidator(isJson=request.is_json, payLoad=data)
        factura_data = validator.validation()
        
        # Calcular el total
        total = 0
        productos_detalle = []
        
        for item in factura_data['productos']:
            producto = MFacturacion.getProductoById(item['producto_id'])
            if not producto:
                return jsonify({"success": False, "message": f"Producto no encontrado"}), 404
            
            # Verificar stock
            if producto['stock'] < item['cantidad']:
                return jsonify({"success": False, "message": f"Stock insuficiente para {producto['nombre']}"}), 400
            
            subtotal = producto['precio'] * item['cantidad']
            total += subtotal
            
            productos_detalle.append({
                'producto_id': item['producto_id'],
                'nombre': producto['nombre'],
                'cantidad': item['cantidad'],
                'precio_unitario': producto['precio'],
                'subtotal': subtotal
            })
            
            # Actualizar stock
            MFacturacion.updateProductoStock(item['producto_id'], producto['stock'] - item['cantidad'])
        
        factura_data['productos'] = productos_detalle
        factura_data['total'] = total
        current_user = get_current_user()
        factura_data['usuario_id'] = current_user.get('user_id')
        # Usar zona horaria de República Dominicana (UTC-4)
        tz_rd = pytz.timezone('America/Santo_Domingo')
        factura_data['fecha'] = datetime.now(tz_rd)
        
        result = MFacturacion.createFactura(factura_data)
        
        return jsonify({
            "success": True,
            "message": "Factura creada exitosamente",
            "factura_id": str(result.inserted_id),
            "total": total
        }), 201
    except ValueError as exc:
        return jsonify({"success": False, "message": str(exc)}), 400
    except Exception as exc:
        return jsonify({"success": False, "message": str(exc)}), 500

@bp.route('/facturas/<factura_id>/descargar', methods=['GET'])
@token_required
def descargar_factura(factura_id):
    try:
        factura = MFacturacion.getFacturaById(factura_id)
        if not factura:
            return jsonify({"success": False, "message": "Factura no encontrada"}), 404
        
        # Obtener información del usuario que facturó
        current_user = get_current_user()
        usuario_nombre = current_user.get('nombre', 'Usuario')
        
        # Crear PDF en memoria
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=letter,
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50
        )
        
        elements = []
        styles = getSampleStyleSheet()
        
        # Estilos personalizados
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=32,
            textColor=colors.HexColor('#0d6efd'),
            spaceAfter=10,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#6c757d'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica'
        )
        
        # Encabezado con logo/nombre
        elements.append(Paragraph("FORPOREA", title_style))
        elements.append(Paragraph("Sistema de Gestión de Embutidos", subtitle_style))
        
        # Línea separadora decorativa
        elements.append(Spacer(1, 0.15*inch))
        line_data = [['']]
        line_table = Table(line_data, colWidths=[7*inch])
        line_table.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 3, colors.HexColor('#0d6efd')),
        ]))
        elements.append(line_table)
        elements.append(Spacer(1, 0.35*inch))
        
        # Información de la factura con mejor diseño
        info_style = ParagraphStyle(
            'InfoLabel',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#6c757d'),
            fontName='Helvetica-Bold'
        )
        
        info_value_style = ParagraphStyle(
            'InfoValue',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#212529'),
            fontName='Helvetica'
        )
        
        # Crear tabla de información con mejor formato
        info_data = [
            [Paragraph('Factura N°:', info_style), Paragraph(str(factura['_id'])[:20] + '...', info_value_style)],
            [Paragraph('Cliente:', info_style), Paragraph(factura['cliente'], info_value_style)],
            [Paragraph('Fecha:', info_style), Paragraph(factura['fecha'].strftime('%d/%m/%Y %H:%M'), info_value_style)],
            [Paragraph('Facturado por:', info_style), Paragraph(usuario_nombre, info_value_style)],
        ]
        
        info_table = Table(info_data, colWidths=[1.5*inch, 5.5*inch])
        info_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('LINEBELOW', (0, 0), (-1, -2), 0.5, colors.HexColor('#e9ecef')),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Título de sección
        section_style = ParagraphStyle(
            'SectionTitle',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#374151'),
            spaceAfter=10,
            fontName='Helvetica-Bold'
        )
        elements.append(Paragraph("DETALLE DE PRODUCTOS", section_style))
        
        # Tabla de productos con mejor diseño
        productos_data = [['Producto', 'Libras', 'Precio/Lb', 'Subtotal']]
        for prod in factura['productos']:
            productos_data.append([
                Paragraph(prod['nombre'], styles['Normal']),
                f"{prod['cantidad']:.2f}",
                f"${prod['precio_unitario']:.2f}",
                f"${prod['subtotal']:.2f}"
            ])
        
        productos_table = Table(productos_data, colWidths=[3.5*inch, 1.0*inch, 1.25*inch, 1.25*inch])
        productos_table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d6efd')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('LEFTPADDING', (0, 0), (0, 0), 12),
            # Body
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 10),
            ('LEFTPADDING', (0, 1), (0, -1), 12),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            # Borders
            ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#dee2e6')),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#0a58ca')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e9ecef')),
        ]))
        elements.append(productos_table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Total con diseño mejorado
        total_style_label = ParagraphStyle(
            'TotalLabel',
            parent=styles['Normal'],
            fontSize=16,
            textColor=colors.HexColor('#212529'),
            fontName='Helvetica-Bold',
            alignment=TA_RIGHT
        )
        
        total_style_value = ParagraphStyle(
            'TotalValue',
            parent=styles['Normal'],
            fontSize=18,
            textColor=colors.HexColor('#0d6efd'),
            fontName='Helvetica-Bold',
            alignment=TA_CENTER
        )
        
        total_data = [[
            Paragraph('TOTAL:', total_style_label),
            Paragraph(f"${factura['total']:.2f}", total_style_value)
        ]]
        
        total_table = Table(total_data, colWidths=[5.5*inch, 1.5*inch])
        total_table.setStyle(TableStyle([
            ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#e7f1ff')),
            ('BOX', (1, 0), (1, 0), 2, colors.HexColor('#0d6efd')),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('LEFTPADDING', (1, 0), (1, 0), 15),
            ('RIGHTPADDING', (1, 0), (1, 0), 15),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
        ]))
        elements.append(total_table)
        
        # Pie de página
        elements.append(Spacer(1, 0.8*inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#6c757d'),
            alignment=TA_CENTER,
            spaceAfter=5
        )
        elements.append(Paragraph("¡Gracias por su compra!", footer_style))
        elements.append(Paragraph("FORPOREA - Sistema de Gestión de Embutidos", footer_style))
        
        # Línea final
        elements.append(Spacer(1, 0.2*inch))
        final_line = Table([['']], colWidths=[7*inch])
        final_line.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 1, colors.HexColor('#dee2e6')),
        ]))
        elements.append(final_line)
        
        # Construir PDF
        doc.build(elements)
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f'Factura_{factura["cliente"]}_{factura["fecha"].strftime("%Y%m%d")}.pdf',
            mimetype='application/pdf'
        )
    except Exception as exc:
        return jsonify({"success": False, "message": str(exc)}), 500
