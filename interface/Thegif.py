import imageio

def in_gif_we_trust(n):
    '''fonction qui transforme les fichier jpeg issus de la simulation en un fichier gif plus visuel pour comprendre le déroulement de la simulation
    :param n: entier correspondant au nombre de tours de la simulation
    :type n: entier
    :return: 
    movie: un fichier gif de la simulation
    '''
    images = []
    for i in range (0,n+1):
        images.append(imageio.imread('Resultats/Image_tour/file{}.jpg'.format(i)))
    imageio.mimsave('Resultats/movie.gif', images)
