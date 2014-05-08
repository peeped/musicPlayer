__author__ = 'liaojie'
#!/usr/bin/env python
#coding:utf-8
import base64
def write_data_to_text_file(filename, list_data):
    f_output = open(filename, 'w+')
    #f_output.write('__align(4) const U8 temp[] = \n')
    #f_output.write('{\n    ')

    f_output.write(list_data)
        #count = 0
    #lenth = len(list_data)
    #for data in list_data:
    #    count += 1
    #    if count != lenth:
    #        f_output.write(data+', ')
    #    else:
    #        f_output.write(data)
    #    if count%16==0:
    #        f_output.write('\n    ')
    #f_output.write('\n};')
    f_output.close()
#
#
#def read_data_from_binary_file(filename, list_data):
#    f = open(filename, 'rb')
#    f.seek(0, 0)
#    #print(len(f))
#    #ss=f.read()
#    #
#    #print ("ssssss",ss)
#    #print ("ssssss")
#    tt=""
#    while True:
#        t_byte = f.read(1)
#        if len(t_byte) == 0:
#            break
#        else:
#            tt+="0x%.2X" % ord(t_byte)
#            list_data.append("0x%.2X" % ord(t_byte))
#    print ("tt",tt)

def thumbnail_string(buf, size=(50, 50)):
    f = StringIO.StringIO(buf)
    image = Image.open(f)
    if image.mode not in ('L', 'RGB'):
        image = image.convert('RGB')
    image = image.resize(size, Image.ANTIALIAS)
    o = StringIO.StringIO()
    image.save(o, "JPEG")
    return o.getvalue()

def main():

    f = open(r'E:/pyPath/musicPlayer/test/05.png','rb')    #用二进制方式打开图片文件
    f.seek(0, 0)
    str = base64.b64encode(f.read()) #读取文件内容，编码为base64字符串
    f.close()

    #print (str)

    #list_data = []
    #read_data_from_binary_file("E:/pyPath/musicPlayer/test/05.png",list_data)
    #convertOneAndZeroToFile("0x5F0x5F0x610x6C0x690x670x6E0x280x340x290x200x630x6F0x6E0x730x740x200x550x380x200x740x650x6D0x700x5B0x5D0x200x3D0x200x0D0x0A0x7B0x0D0x0A0x200x200x200x200x0D0x0A0x7D0x3B",
    #                        "E:/pyPath/musicPlayer/test/06.png")
    #print(list_data)
    #output_f = r'E:/pyPath/musicPlayer/test/05.data'
    #write_data_to_text_file(output_f, list_data)

if __name__ == '__main__':
    main()