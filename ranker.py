import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from sklearn.preprocessing import MinMaxScaler
import time

class TravelRanker:
    def __init__(self, dataset_path):
        self.df = pd.read_csv(dataset_path)
        self.geolocator = Nominatim(user_agent="travel_ranker_app")
        # Cache for coordinates to avoid hitting API limits repeatedly
        self.coord_cache = {} 

    def get_coordinates(self, city_name):
        """Fetches Lat/Long for a city with caching."""
        if city_name in self.coord_cache:
            return self.coord_cache[city_name]
        
        try:
            # Adding 'India' to ensure we get the city in India
            location = self.geolocator.geocode(f"{city_name}, India")
            if location:
                self.coord_cache[city_name] = (location.latitude, location.longitude)
                return self.coord_cache[city_name]
        except Exception as e:
            print(f"Error fetching coordinates for {city_name}: {e}")
        return None

    def calculate_distances(self, source_city):
        """Calculates distance from source_city to all destinations."""
        source_coords = self.get_coordinates(source_city)
        
        if not source_coords:
            raise ValueError(f"Could not find coordinates for source city: {source_city}")

        distances = []
        print(f"📍 Calculating distances from {source_city}...")
        
        # Iterate through unique cities in DB to minimize API calls
        unique_cities = self.df['City'].unique()
        
        for city in unique_cities:
            dest_coords = self.get_coordinates(city)
            if dest_coords:
                dist = geodesic(source_coords, dest_coords).kilometers
            else:
                dist = 10000 # Penalty for unknown locations
            
            # Update all rows matching this city
            self.df.loc[self.df['City'] == city, 'Distance'] = dist
            
            # Sleep briefly to respect API rate limits
            time.sleep(0.1) 

    def rank_destinations(self, source_city, top_n=5):
        # 1. Calculate Distance
        self.calculate_distances(source_city)

        # 2. Data Cleaning: Ensure columns are numeric
        self.df['Google review rating'] = pd.to_numeric(self.df['Google review rating'], errors='coerce')
        self.df['Number of google review in lakhs'] = pd.to_numeric(self.df['Number of google review in lakhs'], errors='coerce')
        
        # 3. Normalization (0 to 1 scale)
        # We need this because Distance (e.g., 200km) is vastly different from Rating (4.5)
        scaler = MinMaxScaler()
        
        # Create a temporary dataframe for scoring
        score_df = self.df.copy()
        score_df[['norm_rating', 'norm_popularity', 'norm_distance']] = scaler.fit_transform(
            score_df[['Google review rating', 'Number of google review in lakhs', 'Distance']]
        )

        # 4. Weighted Scoring Algorithm
        # Weights: Rating (30%), Popularity (20%), Distance (50% - strictly penalize far places for 'weekend')
        w_rating = 0.3
        w_pop = 0.2
        w_dist = 0.5

        # Note: We subtract norm_distance because shorter is better
        score_df['Final_Score'] = (w_rating * score_df['norm_rating']) + \
                                  (w_pop * score_df['norm_popularity']) + \
                                  (1 - (w_dist * score_df['norm_distance']))

        # 5. Sort and Format
        ranked = score_df.sort_values(by='Final_Score', ascending=False).head(top_n)
        
        return ranked[['Name', 'City', 'Type', 'Distance', 'Google review rating', 'Final_Score']]

# --- EXECUTION ---
if __name__ == "__main__":
    ranker = TravelRanker("travel_data.csv")
    
    cities_to_test = ["Delhi", "Mumbai", "Bangalore"]
    
    for source in cities_to_test:
        print(f"\n--- Top Weekend Getaways from {source} ---")
        try:
            results = ranker.rank_destinations(source)
            # Formatting output for better readability
            print(results.to_string(index=False, formatters={
                'Distance': '{:.1f} km'.format,
                'Final_Score': '{:.3f}'.format
            }))
        except Exception as e:
            print(e)