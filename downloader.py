import urllib.request
import time



# url = 'http://www.example.org'
# with urllib.request.urlopen(url) as u:
#  with open('index.html', 'bw') as o:
#    o.write(u.read())

class Task:
    def __init__(self, base_url, base_path, dir, files):
        if base_url[-1] != '/':
            base_url += '/'
        if len(dir) > 0 and dir[-1] != '/':
            dir += '/'
        base_path = base_path.replace('\\', '/')
        if base_path[-1] != '/':
            base_path += '/'
        self._url = base_url
        self._path,  = base_path, 
        self._files = files
        self._dir = dir

    def download(self):
        total = 0
        print('url: {}'.format(self._url + self._dir))
        print('path: {}'.format(self._path + self._dir))
        for file in self._files:
           url = self._url + self._dir + file
           path = self._path + self._dir + file
           url = url.replace(' ', '%20')
           print('file: {} '.format(file))
           start = time.time()
           print('start download')
           with urllib.request.urlopen(url) as u:
               with open(path, 'wb') as o:
                   o.write(u.read())
           cost = time.time() - start
           print('finish download(time: {} sec)'.format(cost))
           total += cost
        print('finish download from url: {}'.format(self._url + self._dir))
        print('total time in this url: {}'.format(total))
        return total


if __name__ == '__main__':
    base_url = 'http://www.azarashin.sakura.ne.jp/github.largefiles/OnlineHackHack/v3PRFdDZ5e5LuheUJCdCCQ73L385uXuJ2B8W/'
    base_path = './'

    tasks = [
        Task(
            base_url, 
            base_path, 
            '', 
            [
                'downloader_target.txt'
            ]), 
        Task(
            base_url, 
            base_path, 
            'documents/RedHackathon/', 
            [
                'final.mp4',
                'movie.mp4',
                'raw_movie.mp4',
                'OnlineHackHack.pptx',
            ]), 
    ]

    total = 0

    for task in tasks:
        total += task.download()

    print('total time: {} sec'.format(total))
