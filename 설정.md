# 초기설정에 대한 정보를 저장합니다.


## 연결 전 기본 설정.
```
    1.필요한 파일 ssh라는 이름의 빈 파일.
    2.네트워크 정보를 담고 있는 wpa_supplicant.conf 파일
    3.config.txt 파일 밑에 dtoverlay=dwc2 라고 추가해준다.
    4.cmdline.txt 파일에서 rootwait 뒤에 modules-load=dwc2,g_ether를 추가해준다.
    
    
```
- wpa_supplicant.conf
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev update_config=1

network={
	ssid="아이디 적고"
	psk="비밀번호 적어주자."
}
```

## 연결 후 설정

1. rndis 드라이버를 사용하여 인터넷을 연결하는 방법.(arp -a 를 사용하거나 bonjour를 설치해서 ip확인)
- (bonjour의 경우 dns-sd -G v4 raspberrypi.local를 입력하여 확인)
2. 노트북의 핫스팟 서비스를 이용하여 인터넷을 연결
- 첫 실습에서는 oled를 위해서 spi를 켜줬음(raspi-config)


- pillow를 사용하여 그림을 그릴 수 있음.
```
sudo apt-get install libjpeg-dev -y
sudo apt-get install zlib1g-dev -y
sudo apt-get install libfreetype6-dev -y
sudo apt-get install liblcms1-dev -y
sudo apt-get install libopenjp2-7 -y
sudo apt-get install libtiff5 -y 
pip3 install pillow 
. 
```

## scp를 이용한 파일 다운로드
```
    라즈베리파이로 복사
    - scp 파일이름 pi@ip주소:폴더이름/
    라즈베리파이에서 복사
    - scp pi@ip주소:파일이름 .(현재 디렉토리를 의미)

```