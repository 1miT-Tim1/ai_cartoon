import os
import cv2
import logging
import numpy as np
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.outputs import OutputKeys

logger = logging.getLogger(__name__)

MODEL_CONFIGS = {
    'anime': {
        'name': '动漫风格',
        'model_id': 'damo/cv_unet_person-image-cartoon_compound-models',
    },
    '3d': {
        'name': '3D风格',
        'model_id': 'damo/cv_unet_person-image-cartoon-3d_compound-models',
    },
    'handdrawn': {
        'name': '手绘风格',
        'model_id': 'damo/cv_unet_person-image-cartoon-handdrawn_compound-models',
    },
    'sketch': {
        'name': '素描风格',
        'model_id': 'damo/cv_unet_person-image-cartoon-sketch_compound-models',
    },
}

_pipelines = {}
_model_errors = {}


def _load_model(model_type):
    """惰性加载指定类型的模型"""
    global _pipelines, _model_errors

    if model_type not in MODEL_CONFIGS:
        raise ValueError(f'不支持的模型类型: {model_type}')

    if model_type in _pipelines and _pipelines[model_type] is not None:
        return True

    if model_type in _model_errors and _model_errors[model_type] is not None:
        return False

    config = MODEL_CONFIGS[model_type]
    try:
        logger.info(f'正在加载 {config["name"]} 模型，请耐心等待...')
        _pipelines[model_type] = pipeline(Tasks.image_portrait_stylization, model=config['model_id'])
        _model_errors[model_type] = None
        logger.info(f'{config["name"]} 模型加载成功')
        return True
    except Exception as e:
        _model_errors[model_type] = str(e)
        _pipelines[model_type] = None
        logger.error(f'{config["name"]} 模型加载失败: {e}')
        return False


def is_model_ready(model_type):
    """检查指定模型是否已就绪"""
    return _load_model(model_type)


def get_model_error(model_type):
    """获取指定模型加载失败的错误信息"""
    return _model_errors.get(model_type)


def get_model_name(model_type):
    """获取模型类型对应的中文名"""
    return MODEL_CONFIGS.get(model_type, {}).get('name', model_type)


def cartoonize(image_path: str, output_path: str, model_type: str = 'anime') -> str:
    """接收图片，调用指定模型卡通化"""
    if not _load_model(model_type):
        model_name = get_model_name(model_type)
        raise RuntimeError(f'{model_name} 模型未就绪: {_model_errors.get(model_type)}')

    model_name = get_model_name(model_type)
    logger.info(f'[{model_name}] 开始卡通化: {image_path}')
    result = _pipelines[model_type](image_path)
    img = result[OutputKeys.OUTPUT_IMG]

    if isinstance(img, np.ndarray):
        cv2.imwrite(output_path, img)
    else:
        raise TypeError(f'模型返回了非预期的数据类型: {type(img)}')

    logger.info(f'[{model_name}] 卡通化完成，结果已保存至: {output_path}')
    return output_path