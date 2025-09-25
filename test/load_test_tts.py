from time import sleep

from components.speaker import generate_and_say, generate_speech

'''
I dont have the official Raspberry Pi 5 PSU available. If I run piper unrestricted on full power, the Raspi dies due to
voltage drops. I need to test if my configuration works without the Pi dying.
'''

i = 0
while i < 100:
    human_rights = '''
    Artikel 1
    Alle Menschen sind frei und gleich an Würde und Rechten geboren. Sie sind mit Vernunft und Gewissen begabt und sollen einander im Geist der Solidarität begegnen.
    
    Artikel 2
    Jeder Mensch hat Anspruch auf die in dieser Erklärung verkündeten Rechte und Freiheiten ohne irgendeinen Unterschied, etwa aufgrund rassistischer Zuschreibungen, nach Hautfarbe, Geschlecht, Sprache, Religion, politischer oder sonstiger Überzeugung, nationaler oder sozialer Herkunft, Vermögen, Geburt oder sonstigem Stand.
    Des Weiteren darf kein Unterschied gemacht werden aufgrund der politischen, rechtlichen oder internationalen Stellung des Landes oder Gebiets, dem eine Person angehört, gleichgültig ob dieses unabhängig ist, unter Treuhandschaft steht, keine Selbstregierung besitzt oder sonst in seiner Souveränität eingeschränkt ist.
    
    Artikel 3
    Jeder Mensch hat das Recht auf Leben, Freiheit und Sicherheit der Person.
    '''
    print(i, "/100")
    i = i + 1
    generate_speech(human_rights)
    sleep(0.5)
