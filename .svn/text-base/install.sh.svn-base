echo export PYTHONPATH=$PYTHONPATH:`pwd`/n-grams:`pwd`/comment_splitter >> ~/.bashrc

# you must run this cript with sudo
echo "Installing sqlite3"
apt-get install sqlite3

echo "Installing MySql"
apt-get install mysql-server-5.1

echo "Installing Python Modules"
apt-get install python-mysqldb
apt-get install python-dateutil

echo "Installing CherryPy"
wget http://download.cherrypy.org/cherrypy/3.1.2/CherryPy-3.1.2.tar.gz
tar -zxf CherryPy-3.1.2.tar.gz
cd CherryPy-3.1.2
python setup.py install
d ..

echo "Fetching solr"
wget http://opensource.become.com/apache/lucene/solr/1.4.0/apache-solr-1.4.0.tgz
tar -zxf apache-solr-1.4.0.tgz

echo "Installing html parsers"
apt-get install libxslt1.1
apt-get install libxslt1-dev
apt-get install libxml++2.6-2
apt-get install libxml++2.6-dev
apt-get install python-setuptools
easy_install lxml
easy_install solrpy

echo "Fetching Heritrix"
wget http://sourceforge.net/projects/archive-crawler/files/archive-crawler%20%28heritrix%201.x%29/1.14.3/heritrix-1.14.3.tar.gz/download
tar -xvzf heritrix-1.14.3.tar.gz



cd updater
mysql -u root -p < createschema.sql

