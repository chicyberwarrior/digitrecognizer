import types
import mmap

class DataSet:
    def __init__(self, name, dataset):
        pass
    
class LabeledDigit:
    def __init__(self, label, data):
        self.label = label
        self.data = data

class MNIST:
    def get_num(self, file_name):
        with open(file_name, "rb+") as f:
            mm = mmap.mmap(f.fileno(), 0)
            
            magic = bytearray(mm[0:4])
            itemsnum = bytearray(mm[4:8])
            
            magic = int(reduce(lambda x, y: (x<<8) + y, magic))
            itemsnum = int(reduce(lambda x, y: (x<<8) + y, itemsnum))
            
            mmap.mmap.close(mm)
            
            return itemsnum
    
    def load_labels(self, file_name):
        with open(file_name, "rb+") as f:
            ll = mmap.mmap(f.fileno(), 0)
            labels = []
            
            magic = bytearray(ll[0:4])
            itemsnum = bytearray(ll[4:8])
            
            magic = int(reduce(lambda x, y: (x<<8) + y, magic))
            itemsnum = int(reduce(lambda x, y: (x<<8) + y, itemsnum))
            
            print "Number of labels: ", itemsnum
            for i in range(0, itemsnum,1):
                num = int(bytearray(ll[8 + i])[0])
                labels.append(num)
                

            print "Done getting labels"
            mmap.mmap.close(ll)
            return labels
        
    def load_images(self, file_name):
        n = self.get_num(file_name)
        
        images = {}
        
        with open(file_name, "rb+") as f:
            mm = mmap.mmap(f.fileno(), 0)
            ''' For each image  '''
            for c in range(0, n, 1):
                
                img = []
                
                ''' For each row '''
                for r in range(0, 28, 1):
                    start = 16 + (c * 28 * 28) + (r * 28)
                    end = start + 28
                            
                    img.extend(bytearray(mm[start:end]) )
                    
                #img = [1 if x > 0 else x for x in img]
                images[c] = img
    
            mmap.mmap.close(mm)
                    
        return images


class DataLoader():
    
    def __init__(self, train_sources, test_sources):
        self.train_sources = train_sources
        self.test_sources = test_sources

    def load(self):

        def test_source(s):
            if s is None:
                raise ValueError, ValueError("Provide filenames containing data")
            
            if not isinstance(s, types.ListType):
                raise ValueError, ValueError("Not a list")

        test_source(self.test_sources)
        test_source(self.train_sources)
        
        m = MNIST()
        imgs = m.load_images(self.train_sources[0][1])
        labels = m.load_labels(self.train_sources[0][0])

        return [LabeledDigit(l, i) for l,i in zip(labels, imgs)]
        #raw_img = imgs[115]
        #
        #for i in range(0, 28):
        #    print raw_img[i * 28: i*28 + 28]
        #
        #import Image
        #img = Image.new("L", (28,28))
        #
        #for i in range(0,28,1):
        #    row = raw_img[i * 28: i*28 + 28]
        #    
        #    for b in range(0, len(row)):
        #        c = row[b]
        #        img.putpixel((b,i), c)
        #        
        #        
        #        
        #print "Saving image "
        #img.save("digit.png")

if __name__ == '__main__':
    dl = DataLoader([("data/train-labels-idx1-ubyte", "data/train-images-idx3-ubyte")], [])
    images = dl.load()