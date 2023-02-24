pipeline {
  agent any

  environment {
    SSH_USER = 'pusula'
    SSH_PASSWORD = 'pusula+2023'
    TARGET_HOST = '192.168.30.21'
  }

  stages {
    stage('Cleanup') {
      steps {
        sh 'rm -rf polr'
      }
    }

    stage('Clone repository') {
      steps {
        sh '''
          git clone https://github.com/badtux66/polr.git polr
        '''
      }
    }

    stage('Install Dependencies') {
      steps {
        sh '''
          cd polr
          composer update
          composer config --no-plugins allow-plugins.kylekatarnls/update-helper true
          composer install
        '''
      }
    }

    stage('Copy .env') {
      steps {
        sh '''
          cd polr
          mv .env.setup .env
        '''
      }
    }

    stage('Set APP_KEY') {
      steps {
        sh '''
          cd polr
          php artisan key:generate
        '''
      }
    }

    stage('Configure Polr') {
      steps {
        sh '''
          cd polr
          sed -i "s/DB_DATABASE=homestead/DB_DATABASE=polr/g" .env
          sed -i "s/DB_USERNAME=homestead/DB_USERNAME=root/g" .env
          sed -i "s/DB_PASSWORD=secret/DB_PASSWORD=pusula_shortener_pass/g" .env
        '''
      }
    }

    stage('Deploy to Target') {
      steps {
        script {
          def sshCommand = "sshpass -p ${env.SSH_PASSWORD} ssh -o StrictHostKeyChecking=no ${env.SSH_USER}@${env.TARGET_HOST}"
          def scpCommand = "sshpass -p ${env.SSH_PASSWORD} scp -o StrictHostKeyChecking=no -r polr ${env.SSH_USER}@${env.TARGET_HOST}:/var/www/html/"

          sh """
            ${sshCommand} <<EOF
            sudo -S dnf remove -y php-common &&
            sudo -S dnf install -y epel-release &&
            sudo -S dnf install -y https://rpms.remirepo.net/enterprise/remi-release-9.rpm &&
            sudo -S dnf module reset -y php &&
            sudo -S dnf module enable -y php:remi-7.4 <<< ${env.SSH_PASSWORD} &&
            sudo -S dnf clean all <<< ${env.SSH_PASSWORD} &&
            sudo -S dnf update -y <<< ${env.SSH_PASSWORD} &&
            sudo -S dnf install -y --skip-broken httpd php php-mysqlnd php-pecl-zip mariadb-server zip unzip <<< ${env.SSH_PASSWORD}
            EOF

            ${scpCommand}

            ${sshCommand} <<EOF
            sudo -S dnf update -y <<< ${env.SSH_PASSWORD} &&
            sudo -S dnf clean all <<< ${env.SSH_PASSWORD} &&
            sudo -S dnf module enable -y php:remi-7.4 <<< ${env.SSH_PASSWORD} &&
            sudo -S dnf install -y --skip-broken httpd php php-mysqlnd php-pecl-zip mariadb-server zip unzip <<< ${env.SSH_PASSWORD} &&
            cd /var/www/html/polr &&
            sudo -S composer install <<< ${env.SSH_PASSWORD} &&
            sudo -S chown -R apache:apache /var/www/html/polr <<< ${env.SSH_PASSWORD} &&
            sudo -S chmod -R 755 /var/www/html/polr <<< ${env.SSH_PASSWORD}
            EOF
          """
        }
      }
    }
  }
}
