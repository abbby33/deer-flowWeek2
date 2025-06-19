#!/usr/bin/env python3
"""
Final Validation Test for Image Generation System
Tests all models, modes, and error handling scenarios
"""

import sys
import os
import time
import traceback
from typing import Dict, Any

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tools.image_generation import (
    get_available_models, 
    create_image_generation_tool,
    GPTImage1Tool,
    JuggernautTool,
    FluxPuLIDTool,
    FluxKontextProTool
)
from schema.model_schemas import MODEL_SCHEMAS

def test_model_discovery():
    print("🔍 Testing Model Discovery...")
    
    try:
        available_models = get_available_models()
        print(f"✅ Found {len(available_models)} available models:")
        for model in available_models:
            print(f"   - {model}")
        
        expected_models = {"gpt-image-1", "juggernaut-xl-v7", "flux-pulid", "flux-kontext-pro"}
        found_models = set(available_models)
        
        if expected_models.issubset(found_models):
            print("✅ All expected models are available")
            return True
        else:
            missing = expected_models - found_models
            print(f"❌ Missing models: {missing}")
            return False
            
    except Exception as e:
        print(f"❌ Model discovery failed: {e}")
        return False

def test_tool_creation():
    print("\n🏭 Testing Tool Creation...")
    
    success_count = 0
    total_tests = 4
    
    test_cases = [
        ("gpt-image-1", GPTImage1Tool),
        ("juggernaut-xl-v7", JuggernautTool), 
        ("flux-pulid", FluxPuLIDTool),
        ("flux-kontext-pro", FluxKontextProTool)
    ]
    
    for model_name, expected_class in test_cases:
        try:
            tool = create_image_generation_tool(model_name)
            if isinstance(tool, expected_class):
                print(f"✅ {model_name}: Created {tool.__class__.__name__}")
                success_count += 1
            else:
                print(f"❌ {model_name}: Expected {expected_class.__name__}, got {tool.__class__.__name__}")
        except Exception as e:
            print(f"❌ {model_name}: Creation failed - {e}")
    
    print(f"📊 Tool Creation: {success_count}/{total_tests} passed")
    return success_count == total_tests

def test_schema_validation():
    """测试模式验证"""
    print("\n📋 Testing Schema Validation...")
    
    success_count = 0
    total_tests = 0
    
    for model_name, schema in MODEL_SCHEMAS.items():
        total_tests += 1
        try:
            tool = create_image_generation_tool(model_name)
            
            if "text" in schema["mode"]:
                test_input = {"prompt": "A beautiful sunset"}
                parsed = tool.parse_agent_input(test_input)
                print(f"✅ {model_name}: Text mode validation passed")
                success_count += 1
            elif "image+text" in schema["mode"]:
                test_input = {
                    "prompt": "A beautiful sunset",
                    "image_ref": "https://example.com/image.jpg"
                }
                parsed = tool.parse_agent_input(test_input)
                print(f"✅ {model_name}: Image+text mode validation passed")
                success_count += 1
                
        except Exception as e:
            print(f"❌ {model_name}: Schema validation failed - {e}")
    
    print(f"📊 Schema Validation: {success_count}/{total_tests} passed")
    return success_count == total_tests

def test_gpt_image_1_generation():
    print("\n🎨 Testing GPT-Image-1 Text-to-Image Generation...")
    
    try:
        tool = create_image_generation_tool("gpt-image-1")
        
        test_input = {
            "prompt": "A serene mountain landscape at sunset with purple clouds",
            "size": "1024x1024",
            "quality": "medium"
        }
        
        print("📝 Input:", test_input)
        print("⏳ Generating image (this may take 10-30 seconds)...")
        
        start_time = time.time()
        result = tool.generate(test_input)
        generation_time = time.time() - start_time
        
        print(f"⏱️ Generation completed in {generation_time:.1f} seconds")
        
        # 验证响应格式
        if isinstance(result, dict) and "image_url" in result:
            print("✅ GPT-Image-1 generation successful")
            print(f"🖼️ Image URL: {result['image_url'][:100]}..." if len(result['image_url']) > 100 else result['image_url'])
            
            if "generation_metadata" in result:
                metadata = result["generation_metadata"]
                print(f"📊 Model: {metadata.get('model', 'unknown')}")
                print(f"📊 Provider: {metadata.get('provider', 'unknown')}")
                print(f"📊 Mode: {metadata.get('mode', 'unknown')}")
            
            return True
        else:
            print(f"❌ Invalid response format: {result}")
            return False
            
    except Exception as e:
        print(f"❌ GPT-Image-1 generation failed: {e}")
        traceback.print_exc()
        return False

def test_juggernaut_generation():
    print("\n🎨 Testing Juggernaut XL v7 Text-to-Image Generation...")
    
    try:
        tool = create_image_generation_tool("juggernaut-xl-v7")
        
        test_input = {
            "prompt": "A futuristic cityscape with flying cars and neon lights",
            "width": 1024,
            "height": 1024,
            "guidance_scale": 7.5,
            "num_inference_steps": 30
        }
        
        print("📝 Input:", test_input)
        print("⏳ Generating image (this may take 30-60 seconds)...")
        
        start_time = time.time()
        result = tool.generate(test_input)
        generation_time = time.time() - start_time
        
        print(f"⏱️ Generation completed in {generation_time:.1f} seconds")
        
        # 验证响应格式
        if isinstance(result, dict) and "image_url" in result:
            print("✅ Juggernaut XL v7 generation successful")
            print(f"🖼️ Image URL: {result['image_url'][:100]}..." if len(result['image_url']) > 100 else result['image_url'])
            
            if "generation_metadata" in result:
                metadata = result["generation_metadata"]
                print(f"📊 Model: {metadata.get('model', 'unknown')}")
                print(f"📊 Provider: {metadata.get('provider', 'unknown')}")
                print(f"📊 Mode: {metadata.get('mode', 'unknown')}")
            
            return True
        else:
            print(f"❌ Invalid response format: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Juggernaut XL v7 generation failed: {e}")
        traceback.print_exc()
        return False

def test_error_handling():
    print("\n🚨 Testing Error Handling...")
    
    success_count = 0
    total_tests = 3
    
    # 无效模型名称
    try:
        tool = create_image_generation_tool("invalid-model")
        print("❌ Should have failed for invalid model")
    except Exception as e:
        print("✅ Correctly rejected invalid model name")
        success_count += 1
    
    #  缺少必需参数
    try:
        tool = create_image_generation_tool("gpt-image-1")
        result = tool.generate({})  # 缺少 prompt
        print("❌ Should have failed for missing prompt")
    except Exception as e:
        print("✅ Correctly rejected missing required parameter")
        success_count += 1
    
    #无效模式组合 - Flux Kontext Pro需要输入图像
    try:
        tool = create_image_generation_tool("flux-kontext-pro")
        result = tool.generate({"prompt": "test"})  # 缺少图像输入
        print("❌ Should have failed for missing image input")
    except Exception as e:
        print("✅ Correctly rejected invalid mode combination")
        success_count += 1
    
    print(f"📊 Error Handling: {success_count}/{total_tests} passed")
    return success_count == total_tests

def run_comprehensive_validation():
    
    print("🚀 Starting Comprehensive Validation Test for Image Generation System")
    print("=" * 70)
    
    test_results = []
    
    # 运行所有测试
    tests = [
        ("Model Discovery", test_model_discovery),
        ("Tool Creation", test_tool_creation), 
        ("Schema Validation", test_schema_validation),
        ("GPT-Image-1 Generation", test_gpt_image_1_generation),
        ("Juggernaut Generation", test_juggernaut_generation),
        ("Error Handling", test_error_handling)
    ]
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            test_results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            test_results.append((test_name, False))
    
    
    print("\n" + "=" * 70)
    print("📊 VALIDATION RESULTS SUMMARY")
    print("=" * 70)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print("-" * 70)
    print(f"🎯 Overall Score: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Image generation system is ready for production!")
    else:
        print("⚠️ Some tests failed. Please review the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_validation()
    sys.exit(0 if success else 1) 