import os
import uuid
from flask import Blueprint, render_template, jsonify, request, send_from_directory, current_app, flash, redirect, url_for
from flask_login import login_required, current_user
from cartoonizer import cartoonize, is_model_ready, get_model_error
from models import db, CartoonImage

main_bp = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """检查文件扩展名是否合法"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main_bp.route('/')
def index():
    """首页"""
    return render_template('index.html')

@main_bp.route('/about')
def about():
    """关于页面"""
    return render_template('about.html')

@main_bp.route('/profile')
@login_required
def profile():
    """个人中心 —— 查看用户生成的图片历史"""
    images = current_user.images.order_by(CartoonImage.created_at.desc()).all()
    return render_template('profile.html', user=current_user, images=images)

@main_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """图片上传并卡通化"""
    if request.method == 'GET':
        return render_template('upload.html')

    if 'image' not in request.files:
        flash('未找到上传文件。', 'danger')
        return redirect(url_for('main.upload'))

    file = request.files['image']
    if file.filename == '':
        flash('请选择一个文件。', 'danger')
        return redirect(url_for('main.upload'))

    if not allowed_file(file.filename):
        flash(f'不支持的文件类型，仅允许: {", ".join(ALLOWED_EXTENSIONS)}', 'danger')
        return redirect(url_for('main.upload'))

    # 保存原始图片
    ext = file.filename.rsplit('.', 1)[1].lower()
    unique_name = f'{uuid.uuid4().hex}.{ext}'
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name)
    file.save(upload_path)

    # 模型就绪检查
    if not is_model_ready():
        flash(f'模型加载失败: {get_model_error()}', 'danger')
        return redirect(url_for('main.upload'))

    # 调用 DCT-Net 卡通化
    result_name = f'{uuid.uuid4().hex}.jpg'
    result_path = os.path.join(current_app.config['RESULT_FOLDER'], result_name)

    try:
        cartoonize(upload_path, result_path)
    except Exception as e:
        flash(f'卡通化处理失败: {str(e)}', 'danger')
        return redirect(url_for('main.upload'))

    cartoon_image = CartoonImage(
        user_id=current_user.id,
        original_filename=file.filename,
        original_path=unique_name,
        result_path=result_name,
    )
    db.session.add(cartoon_image)
    db.session.commit()

    return render_template('result.html',original_url=url_for('main.get_upload', filename=unique_name),
    result_url=url_for('main.get_result', filename=result_name),original_name=file.filename)

@main_bp.route('/uploads/<filename>')
def get_upload(filename):
    """提供上传的原始图片访问"""
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@main_bp.route('/results/<filename>')
def get_result(filename):
    """提供结果图片访问"""
    return send_from_directory(current_app.config['RESULT_FOLDER'], filename)

@main_bp.route('/api/health')
def health_check():
    """健康检查接口"""
    return jsonify({'status': 'ok', 'message': 'Flask MVC app is running'})