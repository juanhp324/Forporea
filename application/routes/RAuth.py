from flask import render_template, request, Blueprint, jsonify, redirect, url_for, session
import infrasture.model.MAuth as MAuth
import domain.VAuth as VAuth

bp = Blueprint('RAuth', __name__)

@bp.route('/Login', methods=['GET'])
def show_login_form():
    return render_template('Auth/Login.html')

@bp.route('/Login', methods=['POST'])
def Login():
    data = request.get_json(silent=True)
    login = VAuth.loginValidator(is_json=request.is_json, payLoad=data)

    try:
        userData = login.validation()
    except ValueError as exc:
        return jsonify({"message": str(exc)}), 400
    except LookupError as exc:
        return jsonify({"message": str(exc)}), 404
    except PermissionError as exc:
        return jsonify({"message": str(exc)}), 401

    session['user_id'] = str(userData['_id'])
    session['email'] = userData['email']
    session['rol'] = userData.get('rol', 'usuario')
    session['nombre'] = userData.get('nombre', 'Usuario')
            
    return jsonify(login.redirect_user()), 200

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('RAuth.show_login_form'))
