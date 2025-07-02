# Denizen Assets 🌍

**Curated city images for hyperlocal user experiences**

Tallyfy Denizen is a free service that returns beautiful, curated Unsplash images for any city in the world. If you have the city and country of a user, you can serve up hyperlocal photos to create smart, personalized imagery for landing pages, applications, signup forms, websites, and more.

[![License: Unsplash](https://img.shields.io/badge/License-Unsplash-brightgreen.svg)](https://unsplash.com/license)
[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![PIL](https://img.shields.io/badge/PIL-Pillow-orange.svg)](https://pillow.readthedocs.io/)

## 🚀 Quick Start

### Using the Denizen API

The easiest way to get location-specific images is through our free API:

```bash
# Get an image for New York City
curl https://denizen.tallyfy.com/
# Redirects to: https://denizen-assets.tallyfy.com/assets-medium/US-NYC-1.jpg

# Get greeting text for a country
curl https://denizen.tallyfy.com/text
# Returns: "Hello" (localized greeting)

# Get metadata about the location
curl https://denizen.tallyfy.com/data
# Returns: JSON with image info and location data
```

### Direct Asset Access

You can also directly access images from this repository:

```html
<!-- Small images (640x480) -->
<img src="https://denizen-assets.tallyfy.com/assets-small/US-SF-2.jpg" alt="San Francisco">

<!-- Medium images (1920x1280) -->
<img src="https://denizen-assets.tallyfy.com/assets-medium/FR-PAR-1.jpg" alt="Paris">

<!-- Large images (2400x1600) -->
<img src="https://denizen-assets.tallyfy.com/assets-large/JP-TOK-3.jpg" alt="Tokyo">
```

## 📍 Available Locations

We have curated images for **40+ countries** and **100+ cities** worldwide:

### 🌎 Countries
- **Americas**: United States, Canada, Brazil, Mexico, Colombia, Argentina
- **Europe**: United Kingdom, France, Germany, Spain, Italy, Poland, Russia, Ukraine
- **Asia**: Japan, China, India, South Korea, Thailand, Vietnam, Philippines, Indonesia
- **Middle East & Africa**: Egypt, Iran, Saudi Arabia, South Africa, Kenya, Nigeria, Ethiopia
- **Oceania**: Australia

### 🏙️ Major Cities
- **USA**: New York, Los Angeles, Chicago, San Francisco, Miami, Boston, Seattle, Austin
- **International**: London, Paris, Tokyo, Sydney, Mumbai, Berlin, Barcelona, Amsterdam

*[View complete list of available locations →](assets/)*

## 🏗️ Repository Structure

```
denizen-assets/
├── assets/          # Source images (original resolution)
├── assets-small/    # Small variants (640×480)
├── assets-medium/   # Medium variants (1920×1280) 
├── assets-large/    # Large variants (2400×1600)
├── resize_assets.py # Image processing script
└── README.md       # This file
```

### 📝 Naming Convention

All images follow a strict naming pattern:

**Format**: `[COUNTRY_CODE]-[CITY_CODE]-[NUMBER].jpg`

**Examples**:
- `US-NYC-1.jpg` → United States, New York City, Image #1
- `FR-PAR-3.jpg` → France, Paris, Image #3  
- `JP-TOK-2.jpg` → Japan, Tokyo, Image #2
- `GB-LON-5.jpg` → Great Britain, London, Image #5

**Special US Format**: `US-[STATE]-[CITY]-[NUMBER].jpg`
- `US-CA-LA-1.jpg` → US, California, Los Angeles, Image #1

## 🛠️ Development

### Prerequisites

- Python 3.7+
- PIL/Pillow library

### Setup

```bash
# Clone the repository
git clone https://github.com/tallyfy/denizen-assets.git
cd denizen-assets

# Install dependencies
pip install Pillow
```

### Adding New Images

1. **Add source images** to the `assets/` directory following the naming convention
2. **Run the resize script** to generate all variants:
   ```bash
   python resize_assets.py
   ```
3. **Verify** all variants were created successfully
4. **Commit** your changes

### Image Processing

The `resize_assets.py` script automatically creates three size variants:

- **Small** (640×480): Thumbnails for compact displays
- **Medium** (1920×1280): Standard web display
- **Large** (2400×1600): High-resolution displays

*All variants preserve the original aspect ratio.*

## 🎨 Usage Examples

### React/JavaScript

```jsx
import React from 'react';

const LocationImage = ({ countryCode, cityCode, imageNumber = 1, size = 'medium' }) => {
  const baseUrl = 'https://denizen-assets.tallyfy.com';
  const imageUrl = `${baseUrl}/assets-${size}/${countryCode}-${cityCode}-${imageNumber}.jpg`;
  
  return (
    <img 
      src={imageUrl} 
      alt={`${cityCode}, ${countryCode}`}
      style={{ width: '100%', height: 'auto' }}
    />
  );
};

// Usage
<LocationImage countryCode="US" cityCode="SF" imageNumber={2} size="medium" />
```

### CSS Background Images

```css
.hero-section {
  background-image: url('https://denizen-assets.tallyfy.com/assets-large/US-NYC-1.jpg');
  background-size: cover;
  background-position: center;
  height: 100vh;
}

/* Responsive images */
@media (max-width: 768px) {
  .hero-section {
    background-image: url('https://denizen-assets.tallyfy.com/assets-small/US-NYC-1.jpg');
  }
}
```

### PHP

```php
<?php
function getDenizenImageUrl($country, $city, $number = 1, $size = 'medium') {
    $baseUrl = 'https://denizen-assets.tallyfy.com';
    return "{$baseUrl}/assets-{$size}/{$country}-{$city}-{$number}.jpg";
}

// Usage
echo '<img src="' . getDenizenImageUrl('FR', 'PAR', 2, 'large') . '" alt="Paris">';
?>
```

### Python

```python
import requests
from PIL import Image
from io import BytesIO

def get_denizen_image(country_code, city_code, image_number=1, size='medium'):
    """Download and return a Denizen image as PIL Image object"""
    base_url = 'https://denizen-assets.tallyfy.com'
    image_url = f'{base_url}/assets-{size}/{country_code}-{city_code}-{image_number}.jpg'
    
    response = requests.get(image_url)
    response.raise_for_status()
    
    return Image.open(BytesIO(response.content))

# Usage
image = get_denizen_image('JP', 'TOK', 3, 'large')
image.show()  # Display the Tokyo image
```

## 🌐 API Integration

For dynamic location detection and automatic image serving, use the [Denizen API](https://github.com/tallyfy/denizen):

```javascript
// Automatically get image based on user's location
fetch('https://denizen.tallyfy.com/data')
  .then(response => response.json())
  .then(data => {
    console.log('User location:', data.location);
    console.log('Recommended image:', data.image_url);
  });
```

## 📄 License & Attribution

### Image Licensing
All images are sourced from [Unsplash](https://unsplash.com) and are free to use under the [Unsplash License](https://unsplash.com/license):

- ✅ **Commercial use permitted**
- ✅ **No attribution required** (but appreciated)
- ✅ **Modification and redistribution allowed**
- ❌ **Cannot be used to replicate Unsplash or similar service**

### Repository License
This repository and its automation scripts are released under the MIT License.

### Attribution Example
While not required, we appreciate attribution:

```html
<!-- Example attribution -->
<p>Photo from <a href="https://github.com/tallyfy/denizen-assets">Denizen Assets</a> 
   by <a href="https://tallyfy.com">Tallyfy</a></p>
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Adding New Locations
1. **Find high-quality images** on Unsplash representing the location
2. **Download and rename** following our naming convention
3. **Add to the `assets/` directory**
4. **Run `python resize_assets.py`** to generate variants
5. **Submit a pull request** with clear description

### Improving Processing
- Enhance the resize script for better performance
- Add new image formats (WebP, AVIF)
- Implement automated quality checks
- Add progressive JPEG encoding

### Guidelines
- Images must be high-quality and representative of the location
- Follow the strict naming convention
- Ensure images are appropriate for business use
- Test locally before submitting

## 🔗 Related Projects

- **[Denizen API](https://github.com/tallyfy/denizen)** - Go microservice that serves these images
- **[Tallyfy Platform](https://tallyfy.com/products/)** - AI-powered workflow automation
- **[Tallyfy Documentation](https://tallyfy.com/products/)** - Complete product documentation

## 📈 Usage Statistics

- **1,000+** curated images
- **40+** countries represented  
- **100+** cities covered
- **Global CDN** distribution via Cloudflare
- **99.9%** uptime SLA

## 🚨 Issues & Support

Encountered a problem or have a feature request?

- **Bug Reports**: [Open an issue](https://github.com/tallyfy/denizen-assets/issues)
- **Feature Requests**: [Start a discussion](https://github.com/tallyfy/denizen-assets/discussions)
- **Business Inquiries**: [Contact Tallyfy](https://tallyfy.com/contact/)

## 🏢 About Tallyfy

[Tallyfy](https://tallyfy.com) is an AI-powered workflow automation platform that helps organizations streamline their business processes. Our mission is to "Run AI-powered operations and save 2 hours per person every day."

**Products:**
- **[Tallyfy Pro](https://tallyfy.com/products/)** - Core workflow automation
- **[Tallyfy Forms](https://tallyfy.com/products/)** - Document management
- **[Tallyfy Booking](https://tallyfy.com/products/)** - Appointment scheduling  
- **[Tallyfy Library](https://tallyfy.com/products/)** - Process templates

---

**Made with ❤️ by the [Tallyfy](https://tallyfy.com) team**

*Denizen Assets is part of Tallyfy's commitment to open-source tools that enhance user experiences worldwide.*
