import tkinter as tk
from PIL import Image, ImageTk
import requests
import io
from artists_data import artists_data

class MyApp:
    def __init__(self, chihiro):
        self.chihiro = chihiro
        self.chihiro.title("Chihiro's artist recommendation")
        self.chihiro.geometry("1100x800")  
        self.chihiro.resizable(False, False)  #non-resizable window

        #image paths
        self.image_paths = [
            "beabadoobee.png",
            "bon iver.png",
            "angus and julia stone.png",
            "bright eyes.png",
            "clairo.png",
            "girl in red.png",
            "gregory alan isakov.png",
            "iron and wine.png",
            "jose gonzalez.png",
            "lana del ray.png",
            "mitski.png",
            "rex orange county.png",
            "sufjan stevens.png",
            "the velvet underground.png",
            "alex g.png",

        ]

        #background image
        background_image_path = "first frame.png"  # Replace with the path to your image
        original_image = Image.open(background_image_path)
        resized_image = original_image.resize((1100, 800), resample=Image.BICUBIC)
        self.background_photo = ImageTk.PhotoImage(resized_image)

        #resized background image 
        self.label_background = tk.Label(chihiro, image=self.background_photo)
        self.label_background.image = self.background_photo
        self.label_background.place(x=0, y=0, relwidth=1, relheight=1)

        #displays the image buttons 
        self.create_image_buttons()

        #entry box for user input 
        self.entry_artist = tk.Entry(chihiro, font=("Helvetica", 16), width=60)
        self.entry_artist.place(relx=0.6, rely=0.80, anchor=tk.CENTER)

        #binds the enter key to fetch artist details 
        self.entry_artist.bind("<Return>", lambda event: self.fetch_artist_details())

        #the quit button
        button_quit = tk.Button(chihiro, text="Quit", command=chihiro.destroy, bg="red", fg="white")
        button_quit.place(relx=0.8, rely=0.7, anchor=tk.S)

    def button_click(self, index):
        def on_image_button_click():
            #gets the artist name based on the order of the pngs
            artist_names = [
                "Beabadoobee", "Bon Iver", "Angus & Julia Stone", "Bright Eyes", "Clairo",
                "Girl in Red", "Gregory Alan Isakov", "Iron & Wine", "José González",
                "Lana Del Rey", "Mitski", "Rex Orange County", "Sufjan Stevens",
                "The Velvet Underground", "Alex G"
            ]

            if 0 <= index < len(artist_names):
                artist_name = artist_names[index]
                self.show_artist_details(artist_name)

        on_image_button_click()

    def create_image_buttons(self):
        #creates the image buttons in a 3x5 grid 
        for i in range(3):  #rows
            for j in range(5):  #columns
                index = i * 5 + j
                if index < len(self.image_paths):
                    image_path = self.image_paths[index]
                    image = Image.open(image_path)
                    
                    #resizes the png to fit the button
                    image = image.resize((100, 100))
                    photo = ImageTk.PhotoImage(image)

                    button = tk.Button(self.chihiro, image=photo, text=f"Button {index + 1}")
                    button.image = photo 
                    button.place(x=j * 120 + 150, y=i * 120 + 150)  #adjusts the position of the buttons on the app

                    #adds the click event so that it fetches the data in artists_data.py
                    button.bind("<Button-1>", lambda event, idx=index: self.button_click(idx))

    def show_artist_details(self, artist_name):
        #when the user inputs an artist name successfully, or when they click a button, this will create a window to display the details of the chosen artist. 
        details_window = tk.Toplevel(self.chihiro)
        details_window.title(f"Details for {artist_name}")
        
        #background color of the new window 
        details_window.configure(bg="#FFE6A6")

        #will still help locate the artist name in the local database even if the user types in lowercase 
        artist_name_lower = artist_name.lower()

        #checks if the chosen artist is in the local database 
        for artist in artists_data:
            if artist['strArtist'].lower() == artist_name_lower:
                
                #displays the artist fanart 
                image_url = artist['strArtistFanart']
                image_data = requests.get(image_url).content
                image = Image.open(io.BytesIO(image_data))

                #resizes the artist image in the new window 
                photo_size = (500, 500)
                image.thumbnail(photo_size)

                photo = ImageTk.PhotoImage(image)
                label_image = tk.Label(details_window, image=photo)
                label_image.image = photo 
                label_image.grid(row=0, column=0, pady=10)

                #displays the artist details 
                details_text = f"Artist Name: {artist['strArtist']}\n"
                details_text += f"Genre: {artist['strGenre']}\n"
                details_text += f"Formed Year: {artist['intFormedYear']}\n"
                details_text += f"Biography: {artist['strBiographyEN']}"

                text_widget = tk.Text(details_window, height=10, width=150, wrap=tk.WORD)
                text_widget.insert(tk.END, details_text)

                #controls the font of the text details and formatting 
                text_widget.tag_configure("bold", font=("Helvetica", 12, "bold"))
                text_widget.tag_configure("normal", font=("Helvetica", 12,))

                #formatting
                text_widget.tag_add("bold", "1.0", "1.13")  #artist name 
                text_widget.tag_add("bold", "2.0", "2.5")   #genre
                text_widget.tag_add("bold", "3.0", "3.12")  #formed year
                text_widget.tag_add("bold", "4.0", "4.11")  #biography

                text_widget.config(state=tk.DISABLED)  #read only 
                text_widget.grid(row=1, column=0, pady=5)

                #added a back button to close the new window 
                back_button = tk.Button(details_window, text="Back", command=details_window.destroy)
                back_button.grid(row=2, column=0, pady=10)

                break
        else:
            #this will show an error msg if the user types in an artist name that does not exist in the local database
            label_error = tk.Label(details_window, text=f"Artist '{artist_name}' not found in the local database")
            label_error.grid(row=2, column=0, pady=10)

    def fetch_artist_details(self):
        #will fetch the artist name that the user has typed in the entry box 
        artist_name = self.entry_artist.get().strip()

        if not artist_name:
            return

        #displays the artist details in user input 
        self.show_artist_details(artist_name)


if __name__ == "__main__":
    chihiro = tk.Tk()
    app = MyApp(chihiro)
    chihiro.mainloop()
