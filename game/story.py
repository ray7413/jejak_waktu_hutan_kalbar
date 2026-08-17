class Chapter:
    def __init__(self, chapter_id, year, title, objective, intro, break_text=""):
        self.id = chapter_id
        self.year = year
        self.title = title
        self.objective = objective
        self.intro = intro
        self.break_text = break_text or "The forest continues to change over time."


class StoryManager:
    def __init__(self):
        self.chapters = [
            Chapter(
                "chapter_1",
                1990,
                "The Forest",
                "Learn to manage the ecosystem and respond to danger.",
                "The forest is still healthy, but small disturbances can become dangerous if left unchecked.",
                "This prototype begins with a controlled learning chapter in West Kalimantan."
            ),
            Chapter(
                "chapter_2",
                1997,
                "Dry Season",
                "Keep the forest resilient before fire damage spreads.",
                "Dry conditions raise fire risk. The player must act quickly to protect vulnerable tiles.",
                "A changing climate and human pressure place stress on the forest."
            ),
            Chapter(
                "chapter_3",
                2005,
                "Restoration",
                "Restore damaged tiles and improve biodiversity.",
                "Burned and degraded zones need patient recovery. Replanting and protection matter here.",
                "Recovery is slow but possible when the ecosystem is supported."
            ),
            Chapter(
                "final_2050",
                2050,
                "Future Pressure",
                "Prepare the forest for the final test of resilience.",
                "A fictional development proposal creates a final management challenge for the forest.",
                "The decisions from earlier years now determine whether the forest survives or degrades."
            ),
        ]
        self.index = 0

    def current(self):
        if self.index >= len(self.chapters):
            return self.chapters[-1]
        return self.chapters[self.index]

    def advance(self):
        self.index = min(self.index + 1, len(self.chapters) - 1)
        return self.current()

    def reset(self):
        self.index = 0

    def at_end(self):
        return self.index >= len(self.chapters) - 1
