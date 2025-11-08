from flask import render_template, request, Blueprint, jsonify, session, send_file
from datetime import datetime
import infrasture.model.MFacturacion as MFacturacion
import domain.VFacturacion as VFacturacion
from domain.VPermisos import requiere_permiso
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
import io
from bson import ObjectId

bp = Blueprint('RFacturacion', __name__)

@bp.route('/facturacion')
def facturacion():
    return render_template('Facturacion.html', active_page='facturacion')

@bp.route('/facturas')
def facturas():
    return render_template('Facturas.html', active_page='facturas')

@bp.route('/get_facturas', methods=['GET'])
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
            
            facturas_list.append({
                '_id': str(factura['_id']),
                'cliente': factura.get('cliente', ''),
                'fecha': factura.get('fecha').strftime('%Y-%m-%d %H:%M') if factura.get('fecha') else '',
                'total': factura.get('total', 0),
                'productos': productos_serializables
            })
        
        return jsonify({"success": True, "facturas": facturas_list})
    except Exception as exc:
        return jsonify({"success": False, "message": str(exc)}), 500

@bp.route('/get_productos_factura', methods=['GET'])
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

@bp.route('/create_factura', methods=['POST'])
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
        factura_data['usuario_id'] = session.get('user_id')
        factura_data['fecha'] = datetime.now()
        
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

@bp.route('/descargar_factura/<factura_id>', methods=['GET'])
def descargar_factura(factura_id):
    try:
        factura = MFacturacion.getFacturaById(factura_id)
        if not factura:
            return jsonify({"success": False, "message": "Factura no encontrada"}), 404
        
        # Crear PDF en memoria
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Estilos personalizados
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#0d6efd'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        # Título
        elements.append(Paragraph("FORPOREA", title_style))
        elements.append(Paragraph("Factura de Venta", styles['Heading2']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Información de la factura
        info_data = [
            ['Factura N°:', str(factura['_id'])],
            ['Cliente:', factura['cliente']],
            ['Fecha:', factura['fecha'].strftime('%d/%m/%Y %H:%M')],
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Tabla de productos
        productos_data = [['Producto', 'Cantidad', 'Precio Unit.', 'Subtotal']]
        for prod in factura['productos']:
            productos_data.append([
                prod['nombre'],
                str(prod['cantidad']),
                f"${prod['precio_unitario']:.2f}",
                f"${prod['subtotal']:.2f}"
            ])
        
        productos_table = Table(productos_data, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
        productos_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d6efd')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(productos_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Total
        total_style = ParagraphStyle(
            'TotalStyle',
            parent=styles['Normal'],
            fontSize=16,
            textColor=colors.HexColor('#0d6efd'),
            alignment=TA_RIGHT,
            fontName='Helvetica-Bold'
        )
        elements.append(Paragraph(f"TOTAL: ${factura['total']:.2f}", total_style))
        
        # Pie de página
        elements.append(Spacer(1, 0.5*inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        elements.append(Paragraph("Gracias por su compra - Forporea", footer_style))
        elements.append(Paragraph("Sistema de Gestión de Embutidos", footer_style))
        
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
