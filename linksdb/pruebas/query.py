from models import Album, Artist
query = Album.select().join(Artist)
qry_filter = (Album.title=="Step Up to the Microphone") & (Artist.name == "Newsboys")
album = query.where(qry_filter).get()
print (album)