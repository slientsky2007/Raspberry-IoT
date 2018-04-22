# Rasyberry-IoT
### 项目基于python3创建，所以请注意使用pip3安装轮子

## 所需硬件设备型号

硬件连接请参考对应硬件引脚图[简书文章](https://www.jianshu.com/u/06e291ec9827).

### 1. Raspberry pi (c)
### 2. ssd1306 128*64 OLED I2C
### 3. DHT22
### 4. 按钮模块
### 5. PMSA003
### 6. CH340 or CP2102 USB to TTL（UAERT）

## 安装应用运行所需依赖库
```sh
sudo apt-get install python3-dev python3-pip libfreetype6-dev libjpeg-dev build-essential
sudo apt-get install libopenjp2-7-dev
sudo apt install libsdl-dev libportmidi-dev libsdl-ttf2.0-dev libsdl-mixer1.2-dev libsdl-image1.2-dev
```

## 安装相关python轮子,安装Adafruit_Python_DHT时连同安装RPi.GPIO
```sh
git clone https://github.com/adafruit/Adafruit_Python_DHT
cd Adafruit_Python_DHT
sudo python3 setup.py install
sudo -H pip3 install psutil
sudo -H pip3 install --upgrade luma.oled
sudo -H pip3 install pyserial
```

## 运行程序
```sh
cd Rasyberry-IoT
python3 main.py
```