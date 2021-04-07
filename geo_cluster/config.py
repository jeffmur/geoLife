## Temporary Path Storage for simple plug-in-play development
import os
import dotenv

dotenv.load_dotenv()

API_KEY = os.getenv("API_KEY")
"""
For gmaps Google Maps API
"""

TO_CLUSTER_TSV = os.getenv("TO_CLUSTER_TSV")
"""
Output of CNN-AE clustering and embedding
"""
