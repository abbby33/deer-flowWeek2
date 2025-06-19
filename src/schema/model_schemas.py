MODEL_SCHEMAS = {
    "flux-pulid": {
        "provider": "replicate",
        "mode": ["image+text"],  # PuLID需要面部图像，一个面部ID定制模型
        "input_fields": {
            "prompt": {"alias": "prompt", "required": True},
            "image_ref": {"alias": "main_face_image", "required": True},  # 面部ID模型需要面部图像
            "num_inference_steps": {"alias": "num_inference_steps", "default": 20},
            "guidance_scale": {"alias": "guidance_scale", "default": 4}
        }
    },
    "juggernaut-xl-v7": {
        "provider": "replicate",
        "mode": ["text"],
        "input_fields": {
            "prompt": {"alias": "prompt", "required": True},
            "negative_prompt": {"alias": "negative_prompt", "required": False},
            "width": {"alias": "width", "default": 512},
            "height": {"alias": "height", "default": 768},
            "style": {"alias": "guidance_scale", "default": 7},
            "steps": {"alias": "num_inference_steps", "default": 25}
        }
    },
    "flux-kontext-pro": {
        "provider": "replicate",
        "mode": ["image+text"],  # 只支持img2img
        "input_fields": {
            "prompt": {"alias": "prompt", "required": True},
            "image_ref": {"alias": "input_image", "required": True},  # Kontext Pro使用input_image
            "mask_image": {"alias": "mask", "required": False},
            "mode": {"alias": "mode", "default": "image-to-image"}
        }
    },
    "gpt-image-1": {  # 这是不同于DALL-E的模型
        "provider": "openai",
        "mode": ["text", "image+text"],  # 支持txt2img和img2img
        "input_fields": {
            "prompt": {"alias": "prompt", "required": True},
            "image_ref": {"alias": "image", "required": False},  # img2img时需要
            "size": {"alias": "size", "default": "1024x1024"},
            "quality": {"alias": "quality", "default": "medium"}  # GPT-Image-1支持的质量等级：low/medium/high/auto
        }
    }
}
