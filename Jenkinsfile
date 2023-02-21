pipeline {
    agent any

    environment {
        SSH_USER = 'pusula'
        SSH_PASSWORD = 'pusula+2023'
    }

    stages {
        stage('Clean Up') {
            steps {
                deleteDir()
            }
        }

        stage('Install PHP and Composer') {
            steps {
                script {
                    sh 'echo "pusula+2023" | sudo -S yum -y install epel-release'
                    sh 'echo "pusula+2023" | sudo -S yum -y install https://rpms.remirepo.net/enterprise/remi-release-8.rpm'
                    sh 'echo "pusula+2023" | sudo -S yum -y install yum-utils'
                    sh 'echo "pusula+2023" | sudo -S yum-config-manager --enable remi-php80'
                    sh 'echo "pusula+2023" | sudo -S yum -y update'
                    sh 'echo "pusula+2023" | sudo -S yum -y install php php-cli php-common php-fpm php-gd php-json php-mbstring php-mysqlnd php-opcache php-pdo php-xml php-tokenizer php-curl unzip'
                    sh 'curl -sS https://getcomposer.org/installer | sudo php -- --install-dir=/usr/local/bin --filename=composer'
                }
            }
        }

        stage('Clone repository') {
            steps {
                sh "PATH=$PATH:/usr/bin git clone -b master https://github.com/badtux66/polr"
            }
        }

        stage('Install dependencies')
