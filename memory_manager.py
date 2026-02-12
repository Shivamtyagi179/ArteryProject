# Artery Memory Manager
# Handles simple self-learning memory using JSON

import json
import os

class MemoryManager:
    def __init__(self, memory_path="data/memory.json"):
        self.memory_path = memory_path
        self.memory = self.load_memory()
        print("[MemoryManager] Loaded")

    def load_memory(self):
        if not os.path.exists(self.memory_path):
            return {}

        try:
            with open(self.memory_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def save_memory(self):
        with open(self.memory_path, "w") as f:
            json.dump(self.memory, f, indent=4)

    def remember(self, command_text):
        if command_text in self.memory:
            self.memory[command_text]["count"] += 1
        else:
            self.memory[command_text] = {
                "count": 1
            }

        self.save_memory()
        print(f"[MemoryManager] Remembered: '{command_text}'")
    def save_note(self, title, content, source):
        if "notes" not in self.memory:
            self.memory["notes"] = []

        self.memory["notes"].append({
            "title": title,
            "content": content[:1000],  # limit
            "source": source
        })

        self.save_memory()
        print(f"[MemoryManager] Note saved: {title}")
