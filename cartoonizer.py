import os
import cv2
import logging
import numpy as np
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.outputs import OutputKeys

logger = logging.getLogger(__name__)
MODEL_ID = 'damo/cv_unet_person-image-cartoon_compound-models'
_pipeline = None
_model_error = None

def _load_model():
    """首次使用时加载 DCT-Net 模型，失败时缓存异常信息"""
    global _pipeline, _model_error
    if _pipeline is not None:
        return True
    if _model_error is not None:
        return False
    try:
        logger.info('正在加载 DCT-Net 模型，首次加载需下载模型文件，请耐心等待...')
        _pipeline = pipeline(Tasks.image_portrait_stylization, model=MODEL_ID)
        logger.info('DCT-Net 模型加载成功')
        return True
    except Exception as e:
        _model_error = str(e)
        logger.error(f'DCT-Net 模型加载失败: {e}')
        return False

def is_model_ready():
    """检查模型是否已就绪"""
    return _load_model()

def get_model_error():
    """获取模型加载失败的错误信息"""
    return _model_error

def cartoonize(image_path: str, output_path: str) -> str:
    """接收图片，调用模型卡通化"""
    if not _load_model():
        raise RuntimeError(f'模型未就绪，无法执行卡通化: {_model_error}')

    logger.info(f'开始卡通化: {image_path}')
    result = _pipeline(image_path)
    img = result[OutputKeys.OUTPUT_IMG]

    if isinstance(img, np.ndarray):
        cv2.imwrite(output_path, img)
    else:
        raise TypeError(f'模型返回了非预期的数据类型: {type(img)}')

    logger.info(f'卡通化完成，结果已保存至: {output_path}')
    return output_path