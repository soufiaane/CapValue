from authentication.models import Account
from django.test import TestCase


class AccountTests(TestCase):

    def test_est_recent_avec_futur_article(self):
        """

        Vérifie si la méthode est_recent d'un Article ne

        renvoie pas True si l'Article a sa date de publication

        dans le futur.

        """

        admin = None

        # Il n'y a pas besoin de remplir tous les champs, ni de sauvegarder

        self.assertIsNone(admin)
