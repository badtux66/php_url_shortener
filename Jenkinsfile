pipeline {
    agent any

    environment {
        SSH_USER = 'pusula'
        SSH_KEY = credentials('polr-deployment-pipeline')
        TARGET_HOST = '192.168.30.21'
        TARGET_DIR = '/var/www/html/polr'
        APP_PORT = 8000
        PHP_VERSION = '7.4.33'
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
                    composer update --no-dev
                    composer config --no-plugins allow-plugins.kylekatarnls/update-helper true
                    composer install --no-dev
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

        stage('Deploy to Target') {
            steps {
                script {
                    try {
                        withCredentials([sshUserPrivateKey(credentialsId: 'polr-deployment-pipeline', keyFileVariable: 'SSH_KEY')]) {
                            sh '''
                                cd polr
                                echo "Creating remote directory: $TARGET_DIR"
                                ssh -o StrictHostKeyChecking=no -i $SSH_KEY $SSH_USER@$TARGET_HOST "sudo mkdir -p $TARGET_DIR && sudo chown $SSH_USER $TARGET_DIR"
                                echo "Copying files to remote server: $TARGET_DIR"
                                scp -v -o StrictHostKeyChecking=no -i $SSH_KEY -r -p polr/* $SSH_USER@$TARGET_HOST:$TARGET_DIR
                                echo "Setting file permissions on remote server: $TARGET_DIR"
                                ssh -o StrictHostKeyChecking=no -i $SSH_KEY $SSH_USER@$TARGET_HOST "cd $TARGET_DIR && sudo chmod -R 755 . && sudo service apache2 restart"
                            '''
                        }
                    } catch (err) {
                        echo "Deployment failed: ${err}"
                        currentBuild.result = 'FAILURE'
                    }
                }
            }
        }
    }
}
