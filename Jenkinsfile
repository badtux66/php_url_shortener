pipeline {
    agent any

    environment {
        SSH_USER = 'pusula'
        SSH_KEY = credentials('polr-deployment-pipeline')
        TARGET_HOST = '192.168.155.21'
        TARGET_DIR = '/var/www/polr'
        APP_PORT = 8000
        PHP_VERSION = '8.0.27'
    }

    stages {
        stage('Cleanup') {
            steps {
                sh'''
                    rm -rf polr
                '''    
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
                    cd /var/lib/jenkins/workspace/polr-deployment-pipeline/polr
                    composer update --no-dev
                    composer config --no-plugins allow-plugins.kylekatarnls/update-helper true
                    composer install --no-dev
                '''
            }
        }

        stage('Copy .env') {
            steps {
                sh '''
                    cd /var/lib/jenkins/workspace/polr-deployment-pipeline/polr
                    cp .env.setup .env
                '''
            }
        }

        stage('SSH to Target') {
            steps {                              
                sh '''
                     cd ~/.ssh
                     ssh -i $SSH_KEY $SSH_USER@$TARGET_HOST                                                                                                
                 '''
            }        
        }
                     
        stage('mkdir & chown Target Directory') {
            steps {
                sh '''
                     cd /var/www/polr
                     sudo mkdir -p $TARGET_DIR && sudo chown $SSH_USER $TARGET_DIR                     
                '''
            }
        }

        stage('Deploy via SCP') {
            steps {
                sh '''                    
                    scp -v -o StrictHostKeyChecking=no -i $SSH_KEY -r -p polr/* $SSH_USER@$TARGET_HOST:$TARGET_DIR
                '''
            }
        }


        stage('Setting File Permissions on the Target Directory') {
            steps {
                sh '''
                     cd $TARGET_DIR && sudo chmod -R 755 . && sudo service httpd restart
                '''
            }
        }

        stage('Cleanup after Deployment') {
            steps {
                sh '''
                    cd polr
                    rm -rf vendor
                    rm -rf composer.lock
                '''
            }
        }
        
        stage('Install Dependencies after Deployment') {
            steps {
                sh '''
                    cd polr
                    composer install --no-dev
                '''
            }
        }

        stage('Run Database Migrations after Deployment') {
            steps {
                sh '''
                    cd polr
                    php artisan migrate --force
                '''
        }        
    }
}
