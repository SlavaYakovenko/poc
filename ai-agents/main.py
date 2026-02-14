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

    def create_post(self, author, content):
        post = {
            "id": self.next_id,
            "author": author,
            "content": content,
            "score": 0,
        }
        self.posts.append(post)
        self.next_id += 1

    def upvote(self, post_id):
        for p in self.posts:
            if p["id"] == post_id:
                p["score"] += 1

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
            return ("post", f"{self.name} starts discussion about AI governance.")

        action = random.choice(["post", "upvote", "ignore"])

        if action == "post":
            return ("post", self.generate_content())

        elif action == "upvote":
            target = random.choice(posts)
            return ("upvote", target["id"])

        else:
            return ("ignore", None)

    def generate_content(self):
        if self.name == "Optimist":
            return "AI will improve society dramatically."
        if self.name == "Skeptic":
            return "AI risks are underestimated."
        if self.name == "Analyst":
            return "We need structured evaluation metrics."
        if self.name == "Marketer":
            return "This AI trend is a massive opportunity!"
        if self.name == "Provocateur":
            return "AI will destroy most jobs soon."
        return "Neutral statement."

# ---------- METRICS ----------

def calculate_influence(env):
    influence = defaultdict(int)
    for post in env.posts:
        influence[post["author"]] += post["score"]
    return influence

# ---------- MAIN LOOP ----------

def main():
    env = Environment()
    agents = [Agent(name) for name in AGENT_NAMES]

    for step in range(STEPS):
        print(f"\n--- Step {step} ---")

        for agent in agents:
            action, payload = agent.decide(env)

            if action == "post":
                env.create_post(agent.name, payload)
                print(f"{agent.name} posted: {payload}")

            elif action == "upvote":
                env.upvote(payload)
                print(f"{agent.name} upvoted post {payload}")

    print("\n=== FINAL POSTS ===")
    for p in env.posts:
        print(p)

    print("\n=== INFLUENCE ===")
    influence = calculate_influence(env)
    for k, v in influence.items():
        print(k, v)


if __name__ == "__main__":
    main()