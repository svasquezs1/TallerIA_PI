import os
import numpy as np
from openai import OpenAI
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from movie.models import Movie


class Command(BaseCommand):
    help = "Compara la similitud entre dos películas y un prompt usando embeddings"

    def handle(self, *args, **kwargs):
        load_dotenv('../openAI.env')
        client = OpenAI(api_key=os.environ.get('openai_apikey'))

        def get_embedding(text):
            response = client.embeddings.create(input=[text], model="text-embedding-3-small")
            return np.array(response.data[0].embedding, dtype=np.float32)

        def cosine_similarity(a, b):
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

        # ✅ Elige dos películas que sí existan en tu base de datos
        movie1 = Movie.objects.get(title="Frankenstein")
        movie2 = Movie.objects.get(title="Cleopatra")

        emb1 = get_embedding(movie1.description)
        emb2 = get_embedding(movie2.description)
        similarity = cosine_similarity(emb1, emb2)
        self.stdout.write(f"🎬 {movie1.title} vs {movie2.title}: {similarity:.4f}")

        prompt = "película de terror con monstruos"
        prompt_emb = get_embedding(prompt)

        sim_prompt_movie1 = cosine_similarity(prompt_emb, emb1)
        sim_prompt_movie2 = cosine_similarity(prompt_emb, emb2)

        self.stdout.write(f"📝 Similitud prompt vs '{movie1.title}': {sim_prompt_movie1:.4f}")
        self.stdout.write(f"📝 Similitud prompt vs '{movie2.title}': {sim_prompt_movie2:.4f}")
        