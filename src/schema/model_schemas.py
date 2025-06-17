MODEL_SCHEMAS = {
    "flux-pulid": {
        "provider": "replicate",
        "mode": ["text", "image+text"],
        "input_fields": {
            "prompt": {"alias": "prompt", "required": True},
            "image_ref": {"alias": "input_image", "required": False},
            "style": {"alias": "style", "default": "photorealistic"}
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
    "kontext-flux": {
        "provider": "replicate",
        "mode": ["text", "image+text"],
        "input_fields": {
            "prompt": {"alias": "prompt", "required": True},
            "image_ref": {"alias": "image", "required": False},
            "mask_image": {"alias": "mask", "required": False},
            "mode": {"alias": "mode", "default": "text-to-image"}
        }
    },
    "chatgpt-image-1": {
        "provider": "openai",
        "mode": ["text"],
        "input_fields": {
            "prompt": {"alias": "prompt", "required": True},
            "size": {"alias": "size", "default": "1024x1024"},
            "quality": {"alias": "quality", "default": "standard"},
            "n": {"alias": "n", "default": 1}
        }
    }
}
