# unsplash_downloader
Downloads high quality, free images from Unsplash for use as backgrounds (or whatever)

# requirements
- python requests
- python

not necessarily in that order, and it doesn't really matter which versions (at time of writing)

# how to
- change `APPLICATION_ID` and `DOWNLOAD_LOCATION` to fit your needs
    - you get `APPLICATION_ID` by going to https://unsplash.com/developers and registering an application - I'm not giving you mine because it'll get abused.
    - `DOWNLOAD_LOCATION` is relative to the location of the script. To download photos to the current directory, change to

        ```
        DOWNLOAD_LOCATION = os.path.abspath(
            os.path.dirname(__file__)
        )
        ```

        You can also just put whatever path you want `DOWNLOAD_LOCATION = '/var/www/pictures/'`, for example. Errors regarding folders/files typically relate to this line. It goes without saying that you'll need the proper permissions for the target directory.

- change the `DOWNLOAD_COUNT` parameter, as well - note that the greater the number, the more batches you'll have to do - this is important because the "free" tier for the API limits you to 50 requests per hour (but that's 1,500 photos so... you probably won't hit that)

- `PHOTO_ORIENTATION` - this can be one of `landscape`, `portrait`, or `squarish` - probably doesn't matter unless you plan on using the photos for phone backgrounds (or vertically positioned monitors).

**finally** run

```$ python backgrounds.py```




