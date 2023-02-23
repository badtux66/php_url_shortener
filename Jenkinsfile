pipeline {
    agent any
    options {
        buildDiscarder(logRotator(numToKeepStr: '3'))
    }
    stages {
        stage('cleanup') {
            steps {
                sh 'rm -rf polr'
            }
        }
        stage('clone repository') {
            steps {
                git branch: 'master',
                    url: 'https://github.com/badtux66/php_url_shortener.git'
            }
        }
        stage('install dependencies') {
            steps {
                sh 'sudo dnf install -y php-cli php-mbstring php-xml php-zip'
                sh 'curl -sS https://getcomposer.org/installer | php'
                sh 'php composer.phar install --no-dev -o'
            }
        }
        stage('configure apache') {
            steps {
                sh 'sudo cp .htaccess.example .htaccess'
                sh 'sudo chown apache:apache storage'
                sh 'sudo chown apache:apache public'
            }
        }
        stage('configure virtual host') {
            steps {
                sh 'sudo cp config.ini.example config.ini'
                sh 'sudo cp config.php.example config.php'
                sh 'sudo cp config.php.example env.php'
                sh 'sudo sed -i \'s/example.com/192.168.30.21/g\' /etc/httpd/conf/httpd.conf'
                sh 'sudo systemctl restart httpd'
            }
        }
        stage('test installation') {
            steps {
                sh 'curl http://192.168.30.21 > index.html'
            }
        }
    }
}
