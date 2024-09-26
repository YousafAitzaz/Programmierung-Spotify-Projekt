import pandas as pd
import os
from tabulate import tabulate
from tqdm import tqdm
import time

class Spotify_App:
       def __init__(self):

                     self.df = pd.read_csv('spotify_dataframe_cleaned.csv')
                     self.favorites_dataframe = pd.read_csv('favorites_dataframe.csv')
                     self.separator = '----------------------'
       def add_song(self, dataframe = None, csv_file = None ):
              print('Add a song')
              song_name = input('Enter a song name: ')
              artist_name = input('Enter a artist name: ')
              album_name = input('Enter a album name: ')
              genre = input('Enter a genre: ')
              new_song = { 'artist_name': [artist_name],'album_name': [album_name], 'track_name': [song_name],  'genre': [genre]}
              new_song_df = pd.DataFrame(new_song)

              if dataframe is None and csv_file is None:
                     dataframe = self.df
              if dataframe is self.df and csv_file is None:
                     new_song_df.to_csv('spotify_dataframe_cleaned.csv', index=False, mode = 'a', header=False)
                     print('New Song added successfully')
              elif dataframe is self.favorites_dataframe and csv_file is  None:
                     new_song_df.to_csv('favorites_dataframe.csv', index=False, mode = 'a', header=False)
                     print('New Song added successfully')
              if csv_file is not None and dataframe is None:

                  new_song_df.to_csv(f'playlists/{csv_file}', index=False, mode='a', header=False)
                  print('New Song added successfully')

       def favorites(self):
              while True:
                  favorites_menu = ['Manage Favorites' ,'(1) Show favorite songs','(2) Show favorite artists', '(3) Show favorite albums', '(4) Show favorite genres', '(5) Add a new favorite song, artist, album, genre', '(6) Search a song in favorites',
                                    '(7) Sort Titles','(8) Back to main menu']
                  [print(x) for x in favorites_menu]
                  choose = input('Choose an option: ')
                  print(self.separator)
                  if choose == '1':

                         track_names = self.favorites_dataframe[['track_name']]
                         print(tabulate(track_names, headers= ['track_name'],tablefmt='fancy_grid'))

                  elif choose == '2':
                         artist_names = self.favorites_dataframe[['artist_name']]
                         print(tabulate(artist_names, headers= ['artist_name'] , tablefmt='fancy_grid'))

                  elif choose == '3':
                         album_names = self.favorites_dataframe[['album_name']]
                         print(tabulate(album_names, headers= ['album_name'], tablefmt='fancy_grid'))

                  elif choose == '4':
                         distinct_genres = self.favorites_dataframe['genre'].unique()
                         distinct_genres_list = [[genre] for genre in distinct_genres]
                         print(tabulate(distinct_genres_list , headers = ['genre'], tablefmt='fancy_grid'))
                         #print(distinct_genres)
                  elif choose == '5':
                         self.add_song(self.favorites_dataframe)
                  elif choose == '6':
                      self.search_song_in_dataframe(self.favorites_dataframe)
                  elif choose == '7':
                      self.sort_songs(self.favorites_dataframe)
                  elif choose == '8':
                      break
                  else:
                      print("Invalid option. Please choose again.")

                  print(self.separator)

       def search_song_in_dataframe(self, dataframe=None):

           if dataframe is None:
               dataframe = self.df
           else:
               dataframe = self.favorites_dataframe

           while True:
               algorithms = ['Algorithms', '(1) Hash Table Search O(1)', '(2) Linear Search', '(3) Back to main menu']
               [print(x) for x in algorithms]
               choose = input('Choose an algorithm: ')

               if choose == '1':
                   song_hash_table = {}
                   for index, row in dataframe.iterrows():
                       track_name = row['track_name']

                       if track_name in song_hash_table:
                           song_hash_table[track_name].append(row)
                       else:
                           song_hash_table[track_name] = [row]
                   song_name = input('Enter a song name: ')
                   search_result = song_hash_table.get(song_name, None)

                   if search_result:
                       print(f"Found {len(search_result)} song(s) matching '{song_name}':")
                       search_result_dataframe = pd.DataFrame(search_result)
                       print(tabulate(search_result_dataframe, headers = search_result_dataframe, tablefmt="fancy_grid"))

                   else:
                       print("Song not found.")
                   print(self.separator)

               elif choose == '2':
                   song_name = input('Enter a song name: ')
                   search_result = []

                   for index, row in dataframe.iterrows():
                       if isinstance(row['track_name'], str) and row['track_name'].lower() == song_name.lower():
                           search_result.append(row)


                   if search_result:
                       print(f"Found {len(search_result)} song(s) matching '{song_name}':")
                       search_result_dataframe = pd.DataFrame(search_result)
                       print(tabulate(search_result_dataframe, headers = search_result_dataframe.columns, tablefmt="fancy_grid"))

                   else:
                       print("Song not found.")
                   print(self.separator)

               elif choose == '3':
                   break

               else:
                   print("Invalid choice. Please try again.")
                   print(self.separator)
       def sort_songs(self, dataframe=None):

           if dataframe is None:
               dataframe = self.df
           else:
               dataframe = self.favorites_dataframe

           choices = ['Sorting Algorithms', '(1) Quick Sort', '(2) Bubble Sort', '(3) Back']
           [print(x) for x in choices]
           print(self.separator)
           choose = input('Choose an option: ')
           dataframe['track_name'] = dataframe['track_name'].fillna('').astype(str)
           track_names = dataframe['track_name'].tolist()

           if choose == '1':
               if len(track_names) <= 1:
                   sorted_track_names = track_names
               else:
                   def quick_sort(arr):
                       if len(arr) <= 1:
                           return arr
                       else:
                           pivot = arr[len(arr) // 2]
                           less_than_pivot = [x for x in arr if x < pivot]
                           equal_to_pivot = [x for x in arr if x == pivot]
                           greater_than_pivot = [x for x in arr if x > pivot]
                           return quick_sort(less_than_pivot) + equal_to_pivot + quick_sort(greater_than_pivot)
                   sorted_track_names = quick_sort(track_names)

               spotify_df_sorted = dataframe.set_index('track_name').loc[sorted_track_names].reset_index()
               print(tabulate(spotify_df_sorted.head(50) , headers= spotify_df_sorted.columns, tablefmt='fancy_grid'))

           elif choose == '2':
               def bubble_sort(arr):
                   start = time.time()
                   n = len(arr)
                   progress_bar = tqdm(total=n, desc = "progress", ncols =80)
                   for i in range(n):
                       for j in range(0, n - i - 1):
                           if arr[j] > arr[j + 1]:
                               arr[j], arr[j + 1] = arr[j + 1], arr[j]
                       progress_bar.update(1)
                   progress_bar.close()
                   end = time.time()
                   print(f"Total search time: {end - start}")
                   return arr

               sorted_track_names = bubble_sort(track_names)
               spotify_df_sorted = dataframe.set_index('track_name').loc[sorted_track_names].reset_index()

               print(tabulate(spotify_df_sorted.head(50) , headers= spotify_df_sorted.columns, tablefmt='psql'))

           elif choose == '3':
               print("Going back to the main menu.")
               return
           else:
               print("Invalid choice. Please try again.")
               print(self.separator)
       def playlists(self):
           def playlists_menu():
               directory = 'playlists'

               all_files = os.listdir(directory)
               csv_files = [file for file in all_files if file.endswith('.csv')]
               print('Playlists')
               file_count = 0
               playlists_dict = {}
               for csv_files in csv_files:
                   print(f"({file_count}) {csv_files}")
                   playlists_dict[file_count] = csv_files
                   file_count += 1
               print(self.separator)
               choose = input('Choose an option: ')
               return choose, playlists_dict

           menu = ['Manage Playlists', '(1) Show all playlists', '(2) Add a  song to a playlist',
                   '(3) Show songs in a playlist', '(4) Delete a playlist', '(5) Create a new playlist', '(6) Back']
           while True:
               [print(x) for x in menu]
               print(self.separator)
               choose = input('Choose an option: ')

               if choose == '1':
                   directory = 'playlists'
                   all_files = os.listdir(directory)
                   csv_files = [file for file in all_files if file.endswith('.csv')]
                   csv_files_dict = pd.DataFrame(csv_files)
                   print('Playlists')
                   print(tabulate(csv_files_dict, headers = csv_files_dict.columns, tablefmt='fancy_grid'))

                   print(self.separator)

               elif choose == '2':
                   print('Choose a playlist to add a song to:')
                   playlist_tuple = playlists_menu()
                   if int(playlist_tuple[0]) in playlist_tuple[1].keys():
                       playlist_dict = playlist_tuple[1]
                       playlist_name = playlist_dict[int(playlist_tuple[0])]
                       self.add_song(csv_file= playlist_name)
                   print(self.separator)

               elif choose == '3':
                   print('Choose a playlist')
                   playlist_tuple = playlists_menu()
                   if int(playlist_tuple[0]) in playlist_tuple[1].keys():
                       playlist = playlist_tuple[1]
                       playlist_name = playlist[int(playlist_tuple[0])]
                       playlist_dataframe = pd.read_csv(f'playlists/{playlist_name}')
                       if not playlist_dataframe.empty:
                           print(tabulate(playlist_dataframe.head(10), headers=playlist_dataframe.columns, tablefmt='fancy_grid'))
                       else:
                           print("No songs in the playlist")
                   print(self.separator)

               elif choose == '4':
                   print('Choose a playlist to delete:')
                   playlist_tuple = playlists_menu()
                   if int(playlist_tuple[0]) in playlist_tuple[1].keys():
                       remove_playlist = playlist_tuple[1]
                       playlist_name = remove_playlist[int(playlist_tuple[0])]
                       os.remove(f'playlists/{playlist_name}')
                       print('removed successfully')
                   print(self.separator)

               elif choose == '5':
                   while True:
                       menu = ['(1) Create a new playlist', '(2) Back']
                       [print(menu) for menu in menu]
                       print(self.separator)
                       choose = input('Choose an option: ')
                       if choose == '1':
                           playlist_name = input('What should the playlist be called?: ')
                           new_playlist_dataframe = pd.DataFrame(columns= ['artists','album_name','track_name','track_genre'])
                           directory = r'playlists'
                           filename = os.path.join(directory, f"{playlist_name}.csv")
                           with open(filename, 'w') as f:
                                new_playlist_dataframe.to_csv(filename, index=False)
                                f.flush()
                           print("Playlist created successfully.")
                           print(self.separator)
                           return
                       elif choose == '2':
                           return

               elif choose == '6':
                   break

def main():
       app = Spotify_App()
       while True:
              menu = ["---Spotify App---","(1) Add a new song", "(2) Manage Favorites", "(3) Search", "(4) Sort Title",
                      "(5) Manage Playlists", "(6) Exit"]
              [print(x) for x in menu]
              choose = input('Choose an option: ')
              print('----------------------')
              if choose == '1':
                     app.add_song()
              elif choose == '2':
                      app.favorites()
              elif choose == '3':
                  app.search_song_in_dataframe()
              elif choose == '4':
                  app.sort_songs()

              elif choose == '5':
                  app.playlists()
              elif choose == '6':
                  break

main()
