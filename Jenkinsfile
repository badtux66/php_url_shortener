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
                    composer install --no-interaction --no-dev --prefer-dist
                '''
            }
        }

        stage('Configure Polr') {
            steps {
                sh '''
                    cd polr
                    mv .env.setup .env
                    php artisan key:generate
                    sed -i "s/DB_DATABASE=homestead/DB_DATABASE=polr/g" .env
                    sed -i "s/DB_USERNAME=homestead/DB_USERNAME=pusula/g" .env
                    sed -i "s/DB_PASSWORD=secret/DB_PASSWORD=pusula_shortener_pass/g" .env
                '''
            }
        }

        stage('Deploy to Target') {
            steps {
                sshPublisher(
                    continueOnError: false,
                    failOnError: true,
                    publishers: [
                        sshPublisherDesc(
                            configName: 'my-ssh-server',
                            verbose: true,
                            transfers: [
                                sshTransfer(
                                    sourceFiles: 'polr/**',
                                    remoteDirectory: '/var/www/html/polr',
                                    cleanRemote: true
                                )
                            ]
                        )
                    ]
                )
            }
        }
    }
}
