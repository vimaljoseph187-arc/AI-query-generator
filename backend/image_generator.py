# # image_generator.py
# import os
# import torch
# from diffusers import StableDiffusionPipeline
# from PIL import Image
# import uuid
# import io
# import base64
# import warnings
# warnings.filterwarnings("ignore")

# class TextToImageGenerator:

#     def __init__(self, model_id="runwayml/stable-diffusion-v1-5", device=None):
     
#         self.model_id = model_id
#         self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
#         self.pipe = None
#         self.output_dir = "generated_images"
        
#         # Create output directory
#         os.makedirs(self.output_dir, exist_ok=True)
        
#         print(f"TextToImageGenerator initialized with device: {self.device}")
    
#     def load_model(self):
      
#         if self.pipe is not None:
#             return self.pipe
            
#         print("Loading Stable Diffusion model... This may take a few minutes on first run...")
        
#         try:
#             self.pipe = StableDiffusionPipeline.from_pretrained(
#                 self.model_id,
#                 torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
#                 safety_checker=None,
#                 requires_safety_checker=False
#             )
#             self.pipe = self.pipe.to(self.device)
            
#             # Enable memory optimization for CPU
#             if self.device == "cpu":
#                 self.pipe.enable_attention_slicing()
            
#             print("✅ Model loaded successfully!")
#             return self.pipe
            
#         except Exception as e:
#             print(f"❌ Error loading model: {e}")
#             raise
    
#     def generate_image(self, prompt, num_inference_steps=30, guidance_scale=7.5,height=512, width=512, seed=None, save=True, return_type='pil'):

#         # Load model if not already loaded
#         if self.pipe is None:
#             self.load_model()
        
#         # Set seed for reproducibility
#         if seed is not None:
#             torch.manual_seed(seed)
#             if self.device == "cuda":
#                 torch.cuda.manual_seed(seed)
        
#         print(f"🎨 Generating image for: '{prompt}'")
        
#         try:
#             # Generate the image
#             with torch.no_grad():
#                 image = self.pipe(
#                     prompt,
#                     num_inference_steps=num_inference_steps,
#                     guidance_scale=guidance_scale,
#                     height=height,
#                     width=width
#                 ).images[0]
            
#             result = {
#                 'success': True,
#                 'prompt': prompt,
#                 'image': image,
#                 'metadata': {
#                     'steps': num_inference_steps,
#                     'guidance_scale': guidance_scale,
#                     'size': f"{width}x{height}",
#                     'seed': seed
#                 }
#             }
            
#             # Save image if requested
#             if save:
#                 filename = f"{self.output_dir}/img_{uuid.uuid4().hex[:8]}.png"
#                 image.save(filename)
#                 result['filename'] = filename
#                 print(f"💾 Image saved to: {filename}")
            
#             # Convert to requested format
#             if return_type == 'bytes':
#                 img_byte_arr = io.BytesIO()
#                 image.save(img_byte_arr, format='PNG')
#                 img_byte_arr.seek(0)
#                 result['image_bytes'] = img_byte_arr.getvalue()
#                 result['image'] = None
                
#             elif return_type == 'base64':
#                 img_byte_arr = io.BytesIO()
#                 image.save(img_byte_arr, format='PNG')
#                 img_byte_arr.seek(0)
#                 result['image_base64'] = base64.b64encode(img_byte_arr.getvalue()).decode()
#                 result['image'] = None
            
#             return result
            
#         except Exception as e:
#             print(f"❌ Error generating image: {e}")
#             return {
#                 'success': False,
#                 'error': str(e),
#                 'prompt': prompt
#             }


# # Create a global instance for easy import
# _default_generator = None

# def get_generator(model_id="runwayml/stable-diffusion-v1-5", device=None):
    
#     global _default_generator
#     if _default_generator is None:
#         _default_generator = TextToImageGenerator(model_id, device)
#     return _default_generator

# def text_to_image(prompt, **kwargs):

#     generator = get_generator()
#     result = generator.generate_image(prompt, **kwargs)
#     if result['success']:
#         return result['image']
#     else:
#         raise Exception(f"Image generation failed: {result.get('error', 'Unknown error')}")

# def text_to_image_base64(prompt, **kwargs):

#     generator = get_generator()
#     result = generator.generate_image(prompt, return_type='base64', **kwargs)
#     if result['success']:
#         return result['image_base64']
#     else:
#         raise Exception(f"Image generation failed: {result.get('error', 'Unknown error')}")

# def text_to_image_bytes(prompt, **kwargs):

#     generator = get_generator()
#     result = generator.generate_image(prompt, return_type='bytes', **kwargs)
#     if result['success']:
#         return result['image_bytes']
#     else:
#         raise Exception(f"Image generation failed: {result.get('error', 'Unknown error')}")


# image_generator_improved.py
import os
import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from PIL import Image, ImageDraw, ImageFont
import uuid
import io
import base64
import warnings
import numpy as np
warnings.filterwarnings("ignore")

class HighQualityImageGenerator:
    """
    High-quality text-to-image generator with improved settings
    """
    
    def __init__(self, model_id="runwayml/stable-diffusion-v1-5", device=None, use_improved_scheduler=True):
        """
        Initialize with high-quality settings
        """
        self.model_id = model_id
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        self.pipe = None
        self.output_dir = "generated_images"
        self.use_improved_scheduler = use_improved_scheduler
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        print(f"🎨 HighQualityImageGenerator initialized")
        print(f"   Device: {self.device}")
        print(f"   Model: {model_id}")
        print(f"   Improved scheduler: {use_improved_scheduler}")
    
    def load_model(self):
        """
        Load the Stable Diffusion model with optimal settings
        """
        if self.pipe is not None:
            return self.pipe
            
        print("📦 Loading Stable Diffusion model... This may take a few minutes...")
        
        try:
            # Load with appropriate dtype
            if self.device == "cuda":
                torch_dtype = torch.float16
            else:
                torch_dtype = torch.float32
            
            self.pipe = StableDiffusionPipeline.from_pretrained(
                self.model_id,
                torch_dtype=torch_dtype,
                safety_checker=None,
                requires_safety_checker=False,
                variant="fp16" if self.device == "cuda" else None
            )
            
            # Use improved scheduler for better quality
            if self.use_improved_scheduler:
                print("   Using DPM++ Scheduler for better quality...")
                self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                    self.pipe.scheduler.config,
                    algorithm_type="dpmsolver++",
                    solver_order=2
                )
            
            self.pipe = self.pipe.to(self.device)
            
            # Enable memory optimization
            if self.device == "cpu":
                self.pipe.enable_attention_slicing()
            
            print("✅ Model loaded successfully!")
            return self.pipe
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise
    
    def enhance_prompt(self, prompt, style=None):
        """
        Enhance prompt with style modifiers for better results
        """
        style_modifiers = {
            'photorealistic': "photorealistic, highly detailed, 8k, professional photography, sharp focus",
            'artistic': "artistic, masterpiece, elegant, creative composition",
            'anime': "anime style, cel shaded, vibrant colors, detailed illustration",
            'oil_painting': "oil painting, artistic, textured, canvas, masterpiece",
            'watercolor': "watercolor painting, artistic, soft colors, paper texture",
            'sketch': "pencil sketch, detailed lines, artistic, grayscale",
            'cinematic': "cinematic, dramatic lighting, movie poster, epic composition",
            'fantasy': "fantasy art, magical, ethereal, detailed, mystical",
            'sci-fi': "sci-fi, futuristic, cyberpunk, neon, highly detailed",
            'minimalist': "minimalist, simple, clean, geometric, modern art"
        }
        
        # Add quality boosters
        quality_boosters = ", highly detailed, sharp focus, 8k resolution, professional quality, masterpiece"
        
        if style and style in style_modifiers:
            enhanced = f"{prompt}, {style_modifiers[style]}{quality_boosters}"
        else:
            enhanced = f"{prompt}{quality_boosters}"
        
        return enhanced
    
    def generate_image(self, 
                      prompt, 
                      num_inference_steps=50,  # Increased for better quality
                      guidance_scale=7.5,
                      height=768,  # Increased for better resolution
                      width=768,
                      seed=None,
                      save=True,
                      return_type='pil',
                      style=None,
                      negative_prompt=None):
        """
        Generate high-quality image from text prompt
        """
        # Load model if not already loaded
        if self.pipe is None:
            self.load_model()
        
        # Enhance prompt for better quality
        enhanced_prompt = self.enhance_prompt(prompt, style)
        
        # Default negative prompt to avoid common issues
        if negative_prompt is None:
            negative_prompt = "blurry, low quality, distorted, ugly, bad anatomy, watermark, signature, text"
        
        # Set seed for reproducibility
        if seed is not None:
            torch.manual_seed(seed)
            if self.device == "cuda":
                torch.cuda.manual_seed(seed)
        
        print(f"🎨 Generating high-quality image...")
        print(f"   Prompt: {prompt}")
        print(f"   Style: {style if style else 'default'}")
        print(f"   Steps: {num_inference_steps}")
        print(f"   Size: {width}x{height}")
        
        try:
            # Generate the image with negative prompt
            with torch.no_grad():
                image = self.pipe(
                    enhanced_prompt,
                    negative_prompt=negative_prompt,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale,
                    height=height,
                    width=width
                ).images[0]
            
            # Post-process for better quality
            image = self.enhance_image_quality(image)
            
            result = {
                'success': True,
                'prompt': prompt,
                'enhanced_prompt': enhanced_prompt,
                'image': image,
                'metadata': {
                    'steps': num_inference_steps,
                    'guidance_scale': guidance_scale,
                    'size': f"{width}x{height}",
                    'seed': seed,
                    'style': style,
                    'model': self.model_id
                }
            }
            
            # Save image if requested
            if save:
                # Save high-quality PNG
                filename = f"{self.output_dir}/img_{uuid.uuid4().hex[:8]}.png"
                image.save(filename, quality=95, optimize=True)
                result['filename'] = filename
                print(f"💾 High-quality image saved to: {filename}")
                
                # Also save a smaller preview
                preview_filename = f"{self.output_dir}/preview_{uuid.uuid4().hex[:8]}.jpg"
                preview = image.copy()
                preview.thumbnail((512, 512))
                preview.save(preview_filename, quality=85)
                result['preview_filename'] = preview_filename
            
            # Convert to requested format
            if return_type == 'bytes':
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='PNG', quality=95)
                img_byte_arr.seek(0)
                result['image_bytes'] = img_byte_arr.getvalue()
                result['image'] = None
                
            elif return_type == 'base64':
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='PNG', quality=95)
                img_byte_arr.seek(0)
                result['image_base64'] = base64.b64encode(img_byte_arr.getvalue()).decode()
                result['image'] = None
            
            # Also return preview if needed
            if return_type == 'preview_base64':
                preview = image.copy()
                preview.thumbnail((512, 512))
                img_byte_arr = io.BytesIO()
                preview.save(img_byte_arr, format='JPEG', quality=85)
                img_byte_arr.seek(0)
                result['preview_base64'] = base64.b64encode(img_byte_arr.getvalue()).decode()
            
            return result
            
        except Exception as e:
            print(f"❌ Error generating image: {e}")
            return {
                'success': False,
                'error': str(e),
                'prompt': prompt
            }
    
    def enhance_image_quality(self, image):
        """
        Post-process image for better quality
        """
        # Convert to numpy for processing
        img_array = np.array(image)
        
        # Simple contrast enhancement (optional)
        # You can add more sophisticated enhancement here
        
        return image
    
    def generate_with_upscale(self, prompt, upscale_factor=2, **kwargs):
        """
        Generate and upscale image
        """
        # First generate at base size
        result = self.generate_image(prompt, **kwargs)
        
        if result['success']:
            image = result['image']
            
            # Simple upscaling (for demonstration)
            new_size = (image.width * upscale_factor, image.height * upscale_factor)
            upscaled = image.resize(new_size, Image.Resampling.LANCZOS)
            
            result['upscaled_image'] = upscaled
            result['metadata']['upscaled'] = True
            result['metadata']['upscale_factor'] = upscale_factor
            
            # Save upscaled version
            if kwargs.get('save', True):
                filename = f"{self.output_dir}/upscaled_{uuid.uuid4().hex[:8]}.png"
                upscaled.save(filename)
                result['upscaled_filename'] = filename
        
        return result


# Global instance
_default_generator = None

def get_generator(high_quality=True):
    """
    Get or create a global generator instance
    """
    global _default_generator
    if _default_generator is None:
        if high_quality:
            _default_generator = HighQualityImageGenerator()
        else:
            _default_generator = HighQualityImageGenerator()  # Always use high quality now
    return _default_generator

def text_to_image(prompt, style=None, **kwargs):
    """
    Generate high-quality image from text
    """
    generator = get_generator()
    result = generator.generate_image(prompt, style=style, **kwargs)
    if result['success']:
        return result['image']
    else:
        raise Exception(f"Image generation failed: {result.get('error', 'Unknown error')}")

def text_to_image_base64(prompt, style=None, **kwargs):
    """
    Generate image and return as base64 string
    """
    generator = get_generator()
    result = generator.generate_image(prompt, style=style, return_type='base64', **kwargs)
    if result['success']:
        return result['image_base64']
    else:
        raise Exception(f"Image generation failed: {result.get('error', 'Unknown error')}")