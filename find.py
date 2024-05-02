import struct
import glob
import sys
import unicodedata

def decode_struct(data):
  ret = []
  i = 0
  while i < len(data):
    tag = data[i:i+4].decode('ascii')
    length = struct.unpack('>I', data[i+4:i+8])[0]
    value = data[i+8:i+8+length]
    value = decode(value, tag=tag)
    #ret.append((tag, value))
    ret.append(value)
    i += 8 + length
  return ret


def decode_unicode(data):
  return data.decode('utf-16-be')


def decode_unsigned(data):
  return struct.unpack('>I', data)[0]


def noop(data):
  return data


DECODE_FUNC_FULL = {
  None: decode_struct,
  'vrsn': decode_unicode,
  'sbav': noop,
}

DECODE_FUNC_FIRST = {
  'o': decode_struct,
  't': decode_unicode,
  'p': decode_unicode,
  'u': decode_unsigned,
  'b': noop,
}

def decode(data, tag=None):
  if tag in DECODE_FUNC_FULL:
    decode_func = DECODE_FUNC_FULL[tag]
  else:
    decode_func = DECODE_FUNC_FIRST[tag[0]]

  return decode_func(data)


def loadcrate(fname):
  with open(fname, 'rb') as f:
    return decode(f.read())

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'usage find.py title' 
        exit
	
    shift = len("Subcrates/")
    song = sys.argv[1]
    crates = [] 
    serato_dir = "/Users/Djin/Music/_Serato_/Subcrates/" 
    files = glob.glob(serato_dir + "*.crate")
    for file in files:
        try:
		decoded = loadcrate(file)
		for entry in decoded:
		    try:
			string = unicodedata.normalize('NFKD', entry[0]).encode('ascii', 'ignore')
			if string.find(song) > -1:
                            pos = file.find("Subcrates") + shift
			    crates.append(file[pos:])
			    break
		    except IndexError:
			pass
        except KeyError:
           pass
    for crate in crates:
        print(crate)
