"""Base lorem provider: words, sentences and paragraphs from a word list."""

from typing import Dict, List, Optional, Sequence

from ...core import BaseProvider


class Provider(BaseProvider):
    """Builds filler text from the locale's ``word_list``."""

    word_list: Sequence[str] = ()
    parts_of_speech: Dict[str, Sequence[str]] = {}
    word_connector = " "
    sentence_punctuation = "."

    def get_words_list(
        self,
        part_of_speech: Optional[str] = None,
        ext_word_list: Optional[Sequence[str]] = None,
    ) -> List[str]:
        """The word pool to draw from.

        ``ext_word_list`` overrides everything; otherwise ``part_of_speech``
        selects a sub-list when the locale defines one.
        """
        if ext_word_list is not None:
            return list(ext_word_list)
        if part_of_speech:
            if part_of_speech not in self.parts_of_speech:
                raise ValueError(f"{part_of_speech!r} is not a part of speech in this locale.")
            return list(self.parts_of_speech[part_of_speech])
        return list(self.word_list)

    def word(self, part_of_speech: Optional[str] = None, ext_word_list: Optional[Sequence[str]] = None) -> str:
        return self.words(1, ext_word_list, part_of_speech)[0]

    def words(
        self,
        nb: int = 3,
        ext_word_list: Optional[Sequence[str]] = None,
        part_of_speech: Optional[str] = None,
        unique: bool = False,
    ) -> List[str]:
        pool = self.get_words_list(part_of_speech, ext_word_list)
        return self.random_elements(pool, length=nb, unique=unique)

    def sentence(
        self,
        nb_words: int = 6,
        variable_nb_words: bool = True,
        ext_word_list: Optional[Sequence[str]] = None,
        part_of_speech: Optional[str] = None,
    ) -> str:
        if nb_words <= 0:
            return ""
        if variable_nb_words:
            nb_words = self._vary(nb_words)
        words = self.words(nb_words, ext_word_list, part_of_speech)
        words[0] = words[0].title()
        return self.word_connector.join(words) + self.sentence_punctuation

    def sentences(self, nb: int = 3, ext_word_list: Optional[Sequence[str]] = None) -> List[str]:
        return [self.sentence(ext_word_list=ext_word_list) for _ in range(nb)]

    def paragraph(
        self,
        nb_sentences: int = 3,
        variable_nb_sentences: bool = True,
        ext_word_list: Optional[Sequence[str]] = None,
    ) -> str:
        if nb_sentences <= 0:
            return ""
        if variable_nb_sentences:
            nb_sentences = self._vary(nb_sentences)
        return " ".join(self.sentences(nb_sentences, ext_word_list=ext_word_list))

    def paragraphs(self, nb: int = 3, ext_word_list: Optional[Sequence[str]] = None) -> List[str]:
        return [self.paragraph(ext_word_list=ext_word_list) for _ in range(nb)]

    def text(self, max_nb_chars: int = 200, ext_word_list: Optional[Sequence[str]] = None) -> str:
        """Text of at most ``max_nb_chars`` characters, ending on a sentence."""
        if max_nb_chars < 5:
            raise ValueError("text() needs at least 5 characters")
        out: List[str] = []
        size = 0
        while size < max_nb_chars:
            piece = self.sentence(ext_word_list=ext_word_list) if max_nb_chars >= 25 else self.word(
                ext_word_list=ext_word_list
            )
            if size + len(piece) + 1 > max_nb_chars:
                break
            out.append(piece)
            size += len(piece) + 1
        if not out:
            return self.word(ext_word_list=ext_word_list)[:max_nb_chars]
        return " ".join(out)

    def _vary(self, value: int, spread: float = 0.4) -> int:
        """Jitter a count by +/- ``spread``, never below one."""
        delta = int(value * spread)
        return max(1, value + self.random_int(-delta, delta))
