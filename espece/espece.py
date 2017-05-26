

class Espece(object):
    def __init__(self, hp, valeur_nutritive, champ_vision, a_jouer, cat):
        self._hp = hp
        self._valeur_nutritive = valeur_nutritive
        self._champ_vision = champ_vision
        self._a_jouer = a_jouer
        self._cat = cat

    @property
    def hp(self):
        return self._hp

    @property
    def valeur_nutritive(self):
        return self._valeur_nutritive

    @property
    def mouvement(self):
        return self._mouvement

    @property
    def champ_vision(self):
        return self._champ_vision

    @property
    def cat(self):
        return self._cat

    @property
    def a_jouer(self):
        return self._a_jouer





    def modification_hp(self, hp):
        """
        Permet de modifier  les hp de l'animal
        :param hp: entier relatif
        :type hp:int
        :return: None
        """
        self._hp += hp
        if self._hp <=0 :
            self.mourir()

    def mourir(self):
        """
        passe  à l'état de cadavre un type d'espèce et le supprime de la base de donnée
        :return:
        """
        self._cat = 'Cadavre'
        self._champ_vision =0
        self._mouvement= 0
        self._a_jouer=True




    def vieillir(self):
        """
        L'animal vivant perd de ses pv tandis  que  le cadavre se décompose, baissant donc sa valeur nutritive.
        :return:
        """
        self._a_jouer =False
        if self.cat == 'Cadavre':
            self._valeur_nutritive += -1
        else:
            self.modification_hp(-2)



