TQDB2026 是基於 2015年開發的tqdb專案(https://github.com/wldtw2008/tqdb) 的新版。
功能與舊版一樣，但主要改變為：
1. 使用 Cassandra 4.1.11
2. 改用 Python3
3. 基於 RedHat 8.10 上的 Podman 搭建 rootless Image/Container 環境提供服務

安裝步驟：
1. 請先安裝好RedHat 8.10，並安裝Podman相關套件
   sudo yum module install -y container-tools
   sudo yum install podman-docker
   
2. 在一般使用者路徑下 git clone tqdb2026
   git clone https://github.com/wldtw2008/tqdb2026 ~/tqdb2026.git
   
3. 安裝相關Podman Image
   podman pull registry.access.redhat.com/ubi8/ubi-init --tls-verify=false
   podman pull cassandra:4.1.11 --tls-verify=false
   
4. 建立 tqdb2026 所需運行的 bui8-init Image
   cd ~/tqdb2026.git/host/buildImage_TQDB2026 ; ./buildImage.sh
   (這個步驟依照 Containerfile 內容，從 bui8-init上搭建 python3 + httpd + crond 環境)

設定步驟：
1. 請依照你的環境，設定 ~/tqdb2026.git/tqdb2026.files/tqdb2026/profile_tqdb.sh
   內容說明如下:
   export CASS_IP=192.168.122.1  #Cassandra IP，通常為HOST IP，但請勿使用127.0.0.1等 localhost
   export CASS_PORT=9042         #Cassandra Port，預設為9042

   export D2TQ_IP=10.229.17.110  #TQDB Server IP，即時行情IP
   export D2TQ_PORT=2001         #TQDB Port，即時行情IP

   export TQDB_DIR=/tqdb2026     #PodmanDocker 內的tqdb2026根目錄，請不要修改
2. 第一次執行cassandra後，需要進去設定 keyspace 與 schema
   先執行./cassandra_attach.sh 進入虛擬內
   執行 # cqlsh 複製貼上以下命令
     CREATE KEYSPACE tqdb1 WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 };

     CREATE TABLE tqdb1.tick (
         symbol text,
         datetime timestamp,
         keyval map<text, double>,
         type int,
         PRIMARY KEY (symbol, datetime)
     );

     CREATE TABLE tqdb1.symbol (
         symbol text PRIMARY KEY,
         keyval map<text, text>
     );

     CREATE TABLE tqdb1.minbar (
         symbol text,
         datetime timestamp,
         close double,
         high double,
         low double,
         open double,
         vol double,
         PRIMARY KEY (symbol, datetime)
     );

     CREATE TABLE tqdb1.secbar (
         symbol text,
         datetime timestamp,
         close double,
         high double,
         low double,
         open double,
         vol double,
         PRIMARY KEY (symbol, datetime)
     );

     CREATE TABLE tqdb1.conf (
         confKey text PRIMARY KEY,
         confVal text
     );

啟動步驟:
1. 啟動Cassandra
   cd ~/tqdb2026.git/host ; ./cassandra_start.sh 
   若有需要連入Cassandra內(如執行cqlsh)，可執行 ./cassandra_attach.sh
   若要停止Cassandra，可執行 ./cassandra_stop.sh
   
2. 待Cassandra啟動後30秒，再啟動TQDB2026
   cd ~/tqdb2026.git/host ; ./tqdb_start.sh
   若有需要連入TQDB2026內，可執行 tqdb_attach.sh
   若要停止TQDB2026，可執行 ./tqdb_stop.sh  
**建議將這兩個start.sh放在 host 的 crontab，開機執行。

資料遷移:
0. 請找任一台主機，容量足夠，且能執行java (java-21-openjdk)
   並去官網下載dsbulk-1.11.2.jar

1. 匯出舊機From_Cassandra_IP
   java -jar dsbulk-1.11.2.jar unload -h [From_Cassandra_IP] -k tqdb1 -t conf -url /tmp/tqdb1.conf
   java -jar dsbulk-1.11.2.jar unload -h [From_Cassandra_IP] -k tqdb1 -t secbar -url /tmp/tqdb1.secbar
   java -jar dsbulk-1.11.2.jar unload -h [From_Cassandra_IP] -k tqdb1 -t symbol -url /tmp/tqdb1.symbol
   java -jar dsbulk-1.11.2.jar unload -h [From_Cassandra_IP] -k tqdb1 -t minbar -url /tmp/tqdb1.minbar

2. 匯入新機To_Cassandra_IP
   java -jar dsbulk-1.11.2.jar load -h [To_Cassandra_IP] -k tqdb1 -t secbar -url /tmp/tqdb1.secbar
   java -jar dsbulk-1.11.2.jar load -h [To_Cassandra_IP] -k tqdb1 -t conf -url /tmp/tqdb1.conf
   java -jar dsbulk-1.11.2.jar load -h [To_Cassandra_IP] -k tqdb1 -t symbol -url /tmp/tqdb1.symbol
   java -jar dsbulk-1.11.2.jar load -h [To_Cassandra_IP] -k tqdb1 -t minbar -url /tmp/tqdb1.minbar

維運注意事項:
1. Cassandra 與 TQDB2026 的時區設定要相同
   並且host要校時，建議在/etc/crontab裡面放入
   */30 * * * *   root   chronyd -q 'server clock.stdtime.gov.tw iburst'
   @reboot        root   sleep 120; chronyd -q 'server clock.stdtime.gov.tw iburst'
2. 注意 cassandra.data 使用的硬碟空間
3. 注意 tqdb2026.oldtick 使用的硬碟空間 (crontab 裡面有刪除過舊的命令)

   
WINDOWS注意事項:
1. 因此專案有symbol-link，也有file mode問題，同時python也有RCLF問題，因此
   不建議使用podman desktop方式在純windows 檔案系統下運作。(問題會多到瘋掉)
   **請使用wsl command line 進入wsl，用git clone 此專案後，搭配podman執行，會容易很多。
1.1 設定systemd為啟動命令: 
   開啟wsl後，請編輯/etc/wsl.conf，設定如下:
   [boot]
   systemd=true
1.2 安裝crond、rsyslog
   sudo yum install crond rsyslog
1.3 編輯排程 /etc/crontab
   @reboot root  sleep 30 ; date >> /tmp/bootup
   @reboot user  sleep 30 ; cd /home/user/tqdb2026.git/host ; ./cassandra_start.sh
   @reboot user  sleep 60 ; cd /home/user/tqdb2026.git/host ; ./tqdb_start.sh
1.4 重啟wsl
   wsl --shutdown
   wsl 
2. 建議 cassandra.data、tqdb2026.oldtick這兩個資料夾改用 softlink方式鏈結到 /mnt/c/AutoTrade/tqdb/下
   這樣資料才是保留在真實硬碟上。
3. 因為Windows WSL 特性，虛擬機網路通聯須繞行真實網卡，所以請執行下面命令
   netsh interface portproxy add v4tov4 listenport=9042 listenaddress=0.0.0.0 connectport=9042 connectaddress=[WLS IP 如 172.18.1.13]
   netsh interface portproxy add v4tov4 listenport=8080 listenaddress=0.0.0.0 connectport=8080 connectaddress=[WLS IP 如 172.18.1.13]
   並調整tqdb_profile.sh 內的IP為真實網卡IP
    


