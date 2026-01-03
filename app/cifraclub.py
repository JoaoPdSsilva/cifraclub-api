"""CifraClub Module (sem Selenium)"""

import requests
from bs4 import BeautifulSoup

CIFRACLUB_URL = "https://www.cifraclub.com.br/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; CifraSync/1.0)"
}

class CifraClub:
    """CifraClub Class"""

    def cifra(self, artist: str, song: str) -> dict:
        """Lê a página HTML e extrai a cifra e metadados da música."""
        result = {}

        url = f"{CIFRACLUB_URL}{artist}/{song}/"
        result["cifraclub_url"] = url

        try:
            response = requests.get(url, headers=HEADERS, timeout=10)

            if response.status_code != 200:
                result["error"] = "Cifra não encontrada"
                return result

            soup = BeautifulSoup(response.text, "html.parser")

            self.get_details(soup, result)
            self.get_cifra(soup, result)

        except Exception as e:
            result["error"] = str(e)

        return result

    def get_details(self, soup, result):
        """Obtém os metadados da música"""

        # Nome da música
        name = soup.find("h1", class_="t1")
        result["name"] = name.text.strip() if name else ""

        # Artista
        artist = soup.find("h2", class_="t3")
        result["artist"] = artist.text.strip() if artist else ""

        # YouTube (se existir)
        player = soup.find("div", class_="player-placeholder")
        if player and player.img:
            img_src = player.img.get("src", "")
            if "/vi/" in img_src:
                cod = img_src.split("/vi/")[1].split("/")[0]
                result["youtube_url"] = f"https://www.youtube.com/watch?v={cod}"

    def get_cifra(self, soup, result):
        """Obtém a cifra da música"""

        cifra_container = soup.find("div", class_="cifra_cnt")

        if not cifra_container:
            result["error"] = "Cifra não encontrada"
            return

        pre = cifra_container.find("pre")

        if pre:
            # Mantém formatação original
            result["cifra"] = pre.get_text().split("\n")
        else:
            result["error"] = "Formato de cifra inválido"
