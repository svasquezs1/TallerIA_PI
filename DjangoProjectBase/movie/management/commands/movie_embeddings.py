import os
import numpy as np
from openai import OpenAI
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from movie.models import Movie


class Command(BaseCommand):
    help = "Genera y almacena los embeddings de todas las películas en la base de datos"

    def handle(self, *args, **kwargs):
        load_dotenv('../openAI.env')
        client = OpenAI(api_key=os.environ.get('openai_apikey'))

        def get_embedding(text):
            response = client.embeddings.create(input=[text], model="text-embedding-3-small")
            return np.array(response.data[0].embedding, dtype=np.float32)

        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies in the database")

        for movie in movies:
            try:
                embedding = get_embedding(movie.description)
                movie.emb = embedding.tobytes()
                movie.save()
                self.stdout.write(self.style.SUCCESS(f"👌 Embedding stored for: {movie.title}"))
            except Exception as e:
                self.stderr.write(f"Failed for {movie.title}: {e}")

        self.stdout.write(self.style.SUCCESS("🌟 Finished generating embeddings for all movies"))