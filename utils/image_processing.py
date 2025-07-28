"""
Image processing utilities for AI classification
Handles image preprocessing, validation, and formatting for machine learning models
"""

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import io
import streamlit as st

# Standard image size for AI models
MODEL_IMAGE_SIZE = (180, 180)
SUPPORTED_FORMATS = ['jpg', 'jpeg', 'png', 'bmp', 'tiff']

def validate_image(image_file):
    """
    Validate uploaded image file
    
    Args:
        image_file: Uploaded file object
        
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        # Check file size (max 10MB)
        if hasattr(image_file, 'size') and image_file.size > 10 * 1024 * 1024:
            return False, "File size too large. Maximum 10MB allowed."
        
        # Try to open image
        image = Image.open(image_file)
        
        # Check format
        if image.format.lower() not in ['jpeg', 'png', 'bmp', 'tiff']:
            return False, f"Unsupported format: {image.format}. Please use JPG, PNG, BMP, or TIFF."
        
        # Check dimensions (minimum size)
        if image.size[0] < 50 or image.size[1] < 50:
            return False, "Image too small. Minimum size is 50x50 pixels."
        
        # Check if image has content
        if image.mode not in ['RGB', 'RGBA', 'L']:
            return False, "Invalid image mode. Please use RGB, RGBA, or grayscale images."
        
        return True, "Valid image"
        
    except Exception as e:
        return False, f"Invalid image file: {str(e)}"

def preprocess_image_for_classification(image_file, target_size=MODEL_IMAGE_SIZE):
    """
    Preprocess image for AI classification models
    
    Args:
        image_file: PIL Image or file-like object
        target_size: Target size tuple (width, height)
        
    Returns:
        numpy.ndarray: Preprocessed image array ready for model input
    """
    try:
        # Handle different input types
        if hasattr(image_file, 'read'):
            # File-like object
            image = Image.open(image_file)
        elif isinstance(image_file, Image.Image):
            # PIL Image object
            image = image_file
        else:
            raise ValueError("Invalid image input type")
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize image to target size
        image_resized = image.resize(target_size, Image.Resampling.LANCZOS)
        
        # Convert to numpy array
        img_array = np.array(image_resized)
        
        # Normalize pixel values to [0, 1]
        img_array = img_array.astype(np.float32) / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
        
    except Exception as e:
        st.error(f"Image preprocessing failed: {str(e)}")
        return None

def enhance_image_quality(image, enhancement_factor=1.2):
    """
    Enhance image quality for better classification results
    
    Args:
        image: PIL Image object
        enhancement_factor: Factor for enhancement (1.0 = no change)
        
    Returns:
        PIL.Image: Enhanced image
    """
    try:
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(image)
        enhanced_image = enhancer.enhance(enhancement_factor)
        
        # Enhance contrast slightly
        enhancer = ImageEnhance.Contrast(enhanced_image)
        enhanced_image = enhancer.enhance(1.1)
        
        # Enhance color saturation
        enhancer = ImageEnhance.Color(enhanced_image)
        enhanced_image = enhancer.enhance(1.1)
        
        return enhanced_image
        
    except Exception as e:
        st.warning(f"Image enhancement failed: {str(e)}")
        return image

def process_image_for_classification(image_file, enhance=True):
    """
    Complete image processing pipeline for classification
    
    Args:
        image_file: Input image file
        enhance: Whether to apply image enhancement
        
    Returns:
        tuple: (processed_array, original_image, preprocessing_info)
    """
    preprocessing_info = {
        'original_size': None,
        'target_size': MODEL_IMAGE_SIZE,
        'enhancement_applied': enhance,
        'preprocessing_steps': []
    }
    
    try:
        # Validate image
        is_valid, message = validate_image(image_file)
        if not is_valid:
            st.error(f"Image validation failed: {message}")
            return None, None, preprocessing_info
        
        # Reset file pointer if needed
        if hasattr(image_file, 'seek'):
            image_file.seek(0)
        
        # Load image
        original_image = Image.open(image_file)
        preprocessing_info['original_size'] = original_image.size
        preprocessing_info['preprocessing_steps'].append("Image loaded successfully")
        
        # Apply enhancement if requested
        if enhance:
            enhanced_image = enhance_image_quality(original_image)
            preprocessing_info['preprocessing_steps'].append("Image enhancement applied")
        else:
            enhanced_image = original_image
        
        # Preprocess for classification
        processed_array = preprocess_image_for_classification(enhanced_image)
        
        if processed_array is not None:
            preprocessing_info['preprocessing_steps'].append("Image preprocessed for classification")
            preprocessing_info['final_shape'] = processed_array.shape
        
        return processed_array, original_image, preprocessing_info
        
    except Exception as e:
        st.error(f"Image processing failed: {str(e)}")
        return None, None, preprocessing_info

def create_image_thumbnail(image, size=(150, 150)):
    """
    Create thumbnail of image for display
    
    Args:
        image: PIL Image object
        size: Thumbnail size tuple
        
    Returns:
        PIL.Image: Thumbnail image
    """
    try:
        thumbnail = image.copy()
        thumbnail.thumbnail(size, Image.Resampling.LANCZOS)
        return thumbnail
    except Exception as e:
        st.warning(f"Thumbnail creation failed: {str(e)}")
        return image

def get_image_info(image):
    """
    Extract detailed information about an image
    
    Args:
        image: PIL Image object
        
    Returns:
        dict: Image information
    """
    try:
        info = {
            'format': image.format,
            'mode': image.mode,
            'size': image.size,
            'width': image.size[0],
            'height': image.size[1],
            'has_transparency': image.mode in ['RGBA', 'LA', 'P'],
            'aspect_ratio': round(image.size[0] / image.size[1], 2)
        }
        
        # Check if image has EXIF data
        if hasattr(image, '_getexif') and image._getexif():
            info['has_exif'] = True
        else:
            info['has_exif'] = False
        
        # Estimate file size if available
        if hasattr(image, 'fp') and hasattr(image.fp, 'seek'):
            current_pos = image.fp.tell()
            image.fp.seek(0, 2)  # Seek to end
            info['estimated_size_bytes'] = image.fp.tell()
            image.fp.seek(current_pos)  # Restore position
        
        return info
        
    except Exception as e:
        st.warning(f"Could not extract image info: {str(e)}")
        return {'error': str(e)}

def apply_image_filters(image, filter_type='none'):
    """
    Apply various filters to enhance image for classification
    
    Args:
        image: PIL Image object
        filter_type: Type of filter to apply
        
    Returns:
        PIL.Image: Filtered image
    """
    try:
        if filter_type == 'none':
            return image
        elif filter_type == 'sharpen':
            return image.filter(ImageFilter.SHARPEN)
        elif filter_type == 'edge_enhance':
            return image.filter(ImageFilter.EDGE_ENHANCE)
        elif filter_type == 'detail':
            return image.filter(ImageFilter.DETAIL)
        elif filter_type == 'smooth':
            return image.filter(ImageFilter.SMOOTH)
        elif filter_type == 'unsharp_mask':
            return image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
        else:
            st.warning(f"Unknown filter type: {filter_type}")
            return image
            
    except Exception as e:
        st.warning(f"Filter application failed: {str(e)}")
        return image

def convert_image_format(image, target_format='RGB'):
    """
    Convert image to target format
    
    Args:
        image: PIL Image object
        target_format: Target color format
        
    Returns:
        PIL.Image: Converted image
    """
    try:
        if image.mode != target_format:
            if target_format == 'RGB' and image.mode == 'RGBA':
                # Handle transparency by adding white background
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[-1])  # Use alpha channel as mask
                return background
            else:
                return image.convert(target_format)
        return image
        
    except Exception as e:
        st.warning(f"Format conversion failed: {str(e)}")
        return image

def save_processed_image(image, filename, quality=95):
    """
    Save processed image to file
    
    Args:
        image: PIL Image object
        filename: Output filename
        quality: JPEG quality (if applicable)
        
    Returns:
        bool: Success status
    """
    try:
        if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
            # Ensure RGB mode for JPEG
            if image.mode != 'RGB':
                image = convert_image_format(image, 'RGB')
            image.save(filename, 'JPEG', quality=quality)
        else:
            image.save(filename)
        
        return True
        
    except Exception as e:
        st.error(f"Failed to save image: {str(e)}")
        return False

def batch_process_images(image_files, enhancement=True):
    """
    Process multiple images for batch classification
    
    Args:
        image_files: List of image files
        enhancement: Whether to apply image enhancement
        
    Returns:
        list: List of (processed_array, filename, info) tuples
    """
    results = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, image_file in enumerate(image_files):
        try:
            status_text.text(f"Processing image {i+1} of {len(image_files)}")
            
            processed_array, original_image, info = process_image_for_classification(
                image_file, enhance=enhancement
            )
            
            if processed_array is not None:
                results.append((processed_array, image_file.name, info))
            
            progress_bar.progress((i + 1) / len(image_files))
            
        except Exception as e:
            st.warning(f"Failed to process {image_file.name}: {str(e)}")
    
    status_text.text("Batch processing complete!")
    progress_bar.empty()
    
    return results

def extract_color_features(image):
    """
    Extract color features from image for analysis
    
    Args:
        image: PIL Image object
        
    Returns:
        dict: Color feature information
    """
    try:
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = convert_image_format(image, 'RGB')
        
        # Get image as numpy array
        img_array = np.array(image)
        
        # Calculate color statistics
        features = {
            'mean_rgb': np.mean(img_array, axis=(0, 1)).tolist(),
            'std_rgb': np.std(img_array, axis=(0, 1)).tolist(),
            'min_rgb': np.min(img_array, axis=(0, 1)).tolist(),
            'max_rgb': np.max(img_array, axis=(0, 1)).tolist()
        }
        
        # Calculate overall brightness
        brightness = np.mean(img_array)
        features['brightness'] = float(brightness)
        
        # Calculate contrast (standard deviation of grayscale)
        gray = np.mean(img_array, axis=2)
        features['contrast'] = float(np.std(gray))
        
        return features
        
    except Exception as e:
        st.warning(f"Color feature extraction failed: {str(e)}")
        return {}
