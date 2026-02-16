import random
from collections import defaultdict

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

    def upvote(self, post_id, voter: Agent):
        for p in self.posts:
            if p["id"] == post_id:
                weight = 1 + voter.influence * 0.05
                p["score"] += weight

    def get_recent_posts(self, limit=5):
        return self.posts[-limit:]

# ---------- AGENT ----------

class Agent:
    def __init__(self, name):
        self.name = name
        self.influence = 0

    def decide(self, env: Environment):
        posts = env.get_recent_posts()

        # If no posts yet → create one
        if not posts:
            content, stance = self.generate_content()
            return ("post", (content, stance))

        action = random.choice(["post", "upvote", "ignore"])

        if action == "post":
            content, stence = self.generate_content()
            return ("post", (content, stence))

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

    def generate_content(self):
        if self.name == "Optimist":
            return "AI will improve society dramatically.", "positive"
        if self.name == "Skeptic":
            return "AI risks are underestimated.", "negative"
        if self.name == "Analyst":
            return "We need structured evaluation metrics.",  "neutral"
        if self.name == "Marketer":
            return "This AI trend is a massive opportunity!", "positive"
        if self.name == "Provocateur":
            return "AI will destroy most jobs soon.", "negative"
        return "Neutral statement.", "neutral"

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
    env = Environment()
    agents = [Agent(name) for name in AGENT_NAMES]

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