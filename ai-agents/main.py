import random
import hashlib
from collections import defaultdict
from llm import generate_post


# ---------- CONFIG ----------

STEPS = 50
AGENT_NAMES = ["Optimist", "Skeptic", "Analyst", "Marketer", "Provocateur"]

# ---------- ENVIRONMENT ----------

class Environment:
    def __init__(self):
        self.posts = []
        self.next_id = 0

    def create_post(self, author, content, stance):
        post = {
            "id": self.next_id,
            "author": author,
            "content": content,
            "score": 0,
            "stance": stance
        }
        self.posts.append(post)
        self.next_id += 1

    def upvote(self, post_id, voter):
        for p in self.posts:
            if p["id"] == post_id:
                weight = 1 + voter.influence * 0.05
                p["score"] += weight

    # def get_recent_posts(self, limit=5):
    #     return self.posts[-limit:]
        
    def get_feed(self, top_k=3, recent_k=2):
        if not self.posts:
            return []

        # Top by score
        sorted_posts = sorted(self.posts, key=lambda p: p["score"], reverse=True)
        top_posts = sorted_posts[:top_k]

        # Most recent
        recent_posts = self.posts[-recent_k:]

        # Merge without duplicates
        seen_ids = set()
        feed = []

        for p in top_posts + recent_posts:
            if p["id"] not in seen_ids:
                feed.append(p)
                seen_ids.add(p["id"])

        return feed

# ---------- AGENT ----------

class Agent:


    def __init__(self, name, stance):
        self.name = name
        self.influence = 0
        self.stance = stance
        self.llm_cache = {}

    def decide(self, env: Environment):
        posts = env.get_feed()

        # If no posts yet → create one
        if not posts:
            feed = env.get_feed()
            content, stance = self.generate_content(feed)
            return ("post", (content, stance))

        action = random.choice(["post", "upvote", "ignore"])

        if action == "post":
            feed = env.get_feed()
            content, stance = self.generate_content(feed)
            return ("post", (content, stance))

        elif action == "upvote":
            preferred = []

            for p in posts:
                if self.name == "Optimist" and p["stance"] == "positive":
                    preferred.append(p)
                elif self.name == "Skeptic" and p["stance"] == "negative":
                    preferred.append(p)
                elif self.name == "Analyst" and p["stance"] == "neutral":
                    preferred.append(p)
                elif self.name == "Marketer" and p["score"] >= 1:
                    preferred.append(p)
                elif self.name == "Provocateur" and p["stance"] == "negative":
                    preferred.append(p)

            BIAS_PROBABILITY = 0.7

            if preferred and random.random() < BIAS_PROBABILITY:
                target = random.choice(preferred)
            else:
                target = random.choice(posts)
            return ("upvote", target["id"])

        else:
            return ("ignore", None)

    def generate_content(self, feed):
        feed_text = "\n".join([f"{p['author']}: {p['content']}" for p in feed])
        feed_hash = hashlib.md5(feed_text.encode()).hexdigest()

        key = (self.name, self.stance, feed_hash)

        if key in self.llm_cache:
            content = self.llm_cache[key]
        else:
            content = generate_post(self.name, self.stance, feed)
            self.llm_cache[key] = content

        return content, self.stance

# ---------- METRICS ----------

def calculate_influence(env):
    influence = defaultdict(int)
    for post in env.posts:
        influence[post["author"]] += post["score"]
    return influence

def update_influence(agents, env):
    influence_map = defaultdict(float)
    for post in env.posts:
        influence_map[post["author"]] += post["score"]

    for agent in agents:
        agent.influence = influence_map[agent.name]

# ---------- MAIN LOOP ----------


def main():
    AGENTS_CONFIG = {
    "Optimist": "positive",
    "Skeptic": "negative",
    "Analyst": "neutral",
    "Marketer": "positive",
    "Provocateur": "negative",
    }

    agents = [Agent(name, AGENTS_CONFIG[name]) for name in AGENT_NAMES]
    env = Environment()

    for step in range(STEPS):
        print(f"\n--- Step {step} ---")

        for agent in agents:
            action, payload = agent.decide(env)

            if action == "post":
                content, stence = payload
                env.create_post(agent.name, content, stence)
                print(f"{agent.name} posted: {payload}")

            elif action == "upvote":
                env.upvote(payload, agent)
                print(f"{agent.name} upvoted post {payload}")

        update_influence(agents, env)

    print("\n=== FINAL POSTS ===")
    for p in env.posts:
        print(p)

    print("\n=== INFLUENCE ===")
    influence = calculate_influence(env)
    for k, v in influence.items():
        print(k, v)


if __name__ == "__main__":
    main()