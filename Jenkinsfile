pipeline {
    agent any
    stages {
        stage('Clone repository') {
            steps {
                sh '''
                    git clone -b master https://github.com/badtux66/polr
                '''
            }
        }
        stage('Install dependencies') {
            steps {
                sh '''
                    cd polr
                    composer install --no-dev
                '''
            }
        }
        stage('Build application') {
            steps {
                sh '''
                    cd polr
                    composer dump-autoload --no-dev --optimize
                '''
            }
        }
        stage('Deploy application') {
            steps {
                sh '''
                    cd polr
                    cp -R . /var/www/gshortener
                '''
            }
        }
        stage('Run migrations') {
            steps {
                sh '''
                    cd /var/www/gshortener
                    php index.php migrate
                '''
            }
        }
    }
}
