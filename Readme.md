#Barista-rpi overview


##ファイル構成
**/home/pi/barista-rpiLogger…**バリスタに関連する実行ファイル等が一式入ったフォルダです。

**/home/pi/barista-rpiLogger/barista-rasp-server**…バリスタからの信号を受けて、ログをサーバーにアップするプログラムです。（開発担当：橋本）

**/home/pi/barista-rpiLogger/groveLogger/groveLogger.py**…Groveからのセンシングデータをbarista-rasp-serverに送信するプログラムです。（開発担当：加治）


## ロガー運用スクリプト
- **ログを開始する: /home/pi/barista-rpiLogger/barista-log-start.sh**
- **ログを停止する: /home/pi/barista-rpiLogger/barista-log-kill.sh**

　

***※以下現行のハード側設定なので、リポジトリには含まれない情報***

##ネットワーク
インターネット接続用Wi-Fi(Wlan0)とアドホック接続用Wi-Fi(Wlan1)があります。
設定は**/etc/network/interfaces**内で設定されています。

###wlan0
見つけたネットワークにDHCPで接続する用です。接続したいSSIDは**/etc/wpa-supplicant/wpa_supplicant.conf**内にあります。

###wlan1
Adhoc用のWi-Fiです。SSIDが**barista-pi**、IPアドレスは**192.168.5.1**に設定してあります。