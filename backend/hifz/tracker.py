class HifzTracker:
    """
    Tracks recitation progress for a single surah and detects skipped,
    repeated, or misordered ayahs.

    Invariants:
        - Ayahs are tracked in the order they appear in the surah.
        - Recitations outside the surah raise errors or are flagged.
    """

    def __init__(self, surah_num: int, total_ayahs: int):
        """
        Initialize the tracker.

        Args:
            surah_num (int): The surah number (1–114).
            total_ayahs (int): Total number of ayahs in this surah.
        """
        self.surah_num = surah_num
        self.total_ayahs = total_ayahs
        self.expected = 1
        self.history = []  # List of tuples: (ayah_num, status)

    def update(self, ayah_num: int) -> str:
        """
        Update tracker with a new recited ayah.

        Args:
            ayah_num (int): The ayah number detected from audio.

        Returns:
            str: One of ["correct", "repeat", "skip", "wrong"]
        """
        if ayah_num == self.expected:
            self.history.append((ayah_num, "correct"))
            self.expected += 1
            return "correct"

        elif ayah_num in [a for a, _ in self.history]:
            self.history.append((ayah_num, "repeat"))
            return "repeat"

        elif ayah_num > self.expected:
            skipped = list(range(self.expected, ayah_num))
            self.history.append((ayah_num, f"skip:{skipped}"))
            self.expected = ayah_num + 1
            return "skip"

        elif ayah_num < self.expected:
            self.history.append((ayah_num, "wrong"))
            return "wrong"
