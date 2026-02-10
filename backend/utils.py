"""
Utility functions for waste classification backend
Provides dustbin color mapping, icons, and awareness tips
"""

def get_dustbin_color(waste_class):
    """
    Map waste class to dustbin color
    
    Args:
        waste_class (str): Waste classification (RECYCLABLE, ORGANIC, HAZARDOUS, GENERAL)
    
    Returns:
        str: Dustbin color (blue/green/red/grey)
    """
    color_mapping = {
        "RECYCLABLE": "blue",
        "ORGANIC": "green",
        "HAZARDOUS": "red",
        "GENERAL": "grey",
        # Fallback mappings
        "BIODEGRADABLE": "green",
    }
    
    return color_mapping.get(waste_class.upper(), "grey")  # Default to general for safety


def get_dustbin_icon(waste_class):
    """
    Get icon name for waste class
    
    Args:
        waste_class (str): Waste classification
    
    Returns:
        str: Icon identifier
    """
    icon_mapping = {
        "RECYCLABLE": "recycle",
        "ORGANIC": "leaf",
        "HAZARDOUS": "warning",
        "GENERAL": "trash",
        "BIODEGRADABLE": "leaf",
    }
    
    return icon_mapping.get(waste_class.upper(), "trash")


def get_fallback_awareness_tip(waste_class):
    """
    Provide detailed awareness tips for waste disposal education
    
    Args:
        waste_class (str): Waste classification
    
    Returns:
        str: Detailed awareness tip with disposal instructions
    """
    tips = {
        "ORGANIC": """🟢 ORGANIC / BIODEGRADABLE WASTE

WHY GREEN DUSTBIN: This item is made of natural materials that decompose through biological processes. Microorganisms break it down into nutrient-rich compost within weeks to months.

PROPER DISPOSAL:
• Place in the GREEN dustbin (wet waste bin)
• Do not mix with plastic or non-biodegradable items
• Can be composted at home or community composting facilities
• Keep separate from dry recyclable waste

EXAMPLES: Food scraps, fruit & vegetable peels, tea bags, coffee grounds, eggshells, garden waste, leaves, flowers, paper napkins, cotton.

ENVIRONMENTAL IMPACT: When organic waste goes to landfills instead of being composted, it produces methane - a greenhouse gas 25x more potent than CO2. Proper composting reduces landfill burden by 30% and creates free fertilizer for plants!

💡 TIP: Start a small compost bin at home - your garden will thank you!""",
        
        "RECYCLABLE": """🔵 RECYCLABLE / DRY WASTE

WHY BLUE DUSTBIN: This material can be collected, processed, and transformed into new products. Recycling conserves natural resources, saves energy, and reduces pollution.

PROPER DISPOSAL:
• Place in the BLUE dustbin (dry waste bin)
• Rinse containers to remove food residue
• Flatten cardboard boxes to save space
• Remove caps from bottles (recycle separately)
• Keep items clean and dry

EXAMPLES: Plastic bottles (PET), glass bottles & jars, aluminum cans, steel/tin cans, cardboard, newspapers, magazines, office paper, cartons, metal containers.

ENVIRONMENTAL IMPACT: Recycling one aluminum can saves enough energy to power a TV for 3 hours. Recycling paper saves 17 trees per ton. Plastic recycling reduces oil consumption and ocean pollution.

💡 TIP: Check the recycling symbol (♻️) and number on plastics - Types 1 (PET) and 2 (HDPE) are most commonly recycled!""",
        
        "HAZARDOUS": """🔴 HAZARDOUS / DANGEROUS WASTE

⚠️ WARNING: This item contains toxic, flammable, corrosive, or reactive materials that pose serious risks to human health and the environment.

PROPER DISPOSAL:
• Place in the RED dustbin or designated hazardous waste collection
• NEVER throw in regular garbage bins
• NEVER burn or bury hazardous waste
• Store safely until you can dispose properly
• Take to authorized e-waste collection centers

EXAMPLES: Batteries (all types), electronic devices, mobile phones, computers, light bulbs (CFL/LED), paint, pesticides, cleaning chemicals, medicines, thermometers, aerosol cans.

ENVIRONMENTAL IMPACT: Hazardous waste can contaminate soil and groundwater for decades. One battery can pollute 1 million liters of water. Electronic waste contains lead, mercury, and cadmium that cause serious health problems.

⚠️ CRITICAL: Never mix hazardous items with other waste. Handle with care and dispose at authorized collection points only!

💡 TIP: Many electronics stores and pharmacies accept old batteries and e-waste for safe recycling.""",

        "GENERAL": """⬜ GENERAL / NON-RECYCLABLE WASTE

WHY GREY DUSTBIN: This item cannot be easily recycled or composted with current technology. It requires proper disposal in the general waste stream.

PROPER DISPOSAL:
• Place in the GREY dustbin (general waste bin)
• Reduce usage of such items when possible
• Look for recyclable alternatives
• Do not mix with organic or recyclable waste

EXAMPLES: Chip bags, snack wrappers, tissues, sanitary products, diapers, rubber items, ceramics, broken toys, styrofoam, multi-layered packaging, candy wrappers, cigarette butts.

ENVIRONMENTAL IMPACT: General waste typically ends up in landfills where it can take hundreds of years to decompose. Multi-layered packaging like chip bags combines plastic and aluminum, making recycling nearly impossible.

💡 TIP: Choose products with less packaging and opt for recyclable alternatives when available. Every small choice adds up!"""
    }
    
    return tips.get(waste_class.upper(), """⚠️ UNIDENTIFIED ITEM

For your safety and environmental protection, when the waste type cannot be determined with certainty:

RECOMMENDED ACTION:
• Treat as HAZARDOUS waste (RED dustbin)
• Do not mix with regular household waste
• Check with local waste management authority
• Look for disposal instructions on the product packaging

When in doubt, it's always safer to handle unknown waste as potentially hazardous rather than risk contaminating recyclable or organic waste streams.

💡 TIP: Take a photo and consult your local municipal waste guide for proper disposal instructions.""")


def validate_image_format(filename):
    """
    Validate if uploaded file is an image
    
    Args:
        filename (str): Name of the uploaded file
    
    Returns:
        bool: True if valid image format, False otherwise
    """
    if not filename:
        return False
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'jfif', 'pjpeg', 'pjp'}
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in allowed_extensions


def get_class_description(waste_class):
    """
    Get detailed description of waste class
    
    Args:
        waste_class (str): Waste classification
    
    Returns:
        str: Detailed description
    """
    descriptions = {
        "RECYCLABLE": "Materials that can be reprocessed and reused. Examples: plastic bottles, glass, metal cans, cardboard.",
        
        "ORGANIC": "Organic waste that decomposes naturally through biological processes. Examples: food scraps, leaves, garden waste.",
        
        "HAZARDOUS": "Waste that poses risks to health or environment. Examples: batteries, chemicals, medical waste, e-waste.",
        
        "GENERAL": "Non-recyclable items that go to landfill. Examples: chip bags, tissues, multi-layered wrappers."
    }
    
    return descriptions.get(waste_class.upper(), "Unknown waste category.")


def normalize_class_name(yolo_class_name):
    """
    Normalize YOLO model output to standard categories
    Maps model output to display names (RECYCLABLE/ORGANIC/HAZARDOUS/GENERAL)
    
    Args:
        yolo_class_name (str): Class name from YOLO model
    
    Returns:
        str: Normalized category
    """
    normalized = yolo_class_name.upper().strip()
    
    # Direct mappings for standard class names
    if normalized == "RECYCLABLE":
        return "RECYCLABLE"
    
    if normalized == "ORGANIC":
        return "ORGANIC"
    
    # Map BIODEGRADABLE to ORGANIC for display
    if normalized == "BIODEGRADABLE":
        return "ORGANIC"
    
    if normalized == "HAZARDOUS":
        return "HAZARDOUS"
    
    if normalized == "GENERAL":
        return "GENERAL"
    
    # Fallback: try keyword matching for robustness
    # Recyclable variations
    recyclable_keywords = ['RECYCLABLE', 'RECYCLE', 'PLASTIC', 'PAPER', 'GLASS', 'METAL', 'CARDBOARD', 'ALUMINUM', 'CAN', 'BOTTLE']
    if any(keyword in normalized for keyword in recyclable_keywords):
        return "RECYCLABLE"
    
    # Organic/Biodegradable variations
    organic_keywords = ['ORGANIC', 'BIODEGRADABLE', 'COMPOST', 'FOOD', 'GARDEN', 'LEAF', 'LEAVES', 'WOOD']
    if any(keyword in normalized for keyword in organic_keywords):
        return "ORGANIC"
    
    # Hazardous variations
    hazardous_keywords = ['HAZARDOUS', 'HAZARD', 'BATTERY', 'CHEMICAL', 'MEDICAL', 'E-WASTE', 'TOXIC', 'PAINT', 'BULB']
    if any(keyword in normalized for keyword in hazardous_keywords):
        return "HAZARDOUS"
    
    # General waste variations
    general_keywords = ['GENERAL', 'TRASH', 'TISSUE', 'WRAPPER', 'CHIP', 'SNACK', 'STYROFOAM']
    if any(keyword in normalized for keyword in general_keywords):
        return "GENERAL"
    
    # Default to GENERAL for unknown items
    return "GENERAL"

