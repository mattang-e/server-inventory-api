pipeline {
    agent any

    environment {
        HARBOR_REGISTRY = 'harbor.lab.local'
        HARBOR_PROJECT = 'server-inventory'
        IMAGE_NAME = 'server-inventory-api'
    }

    stages {
        stage('Checkout Test') {
            steps {
                sh 'echo "Git checkout successful"'
                sh 'whoami'
                sh 'pwd'
                sh 'ls -al'
            }
        }

        stage('Build Image') {
            steps {
                sh '''
                    podman build \
                        -t ${HARBOR_REGISTRY}/${HARBOR_PROJECT}/${IMAGE_NAME}:${BUILD_NUMBER} .
                '''
            }
        }

        stage('Push Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'harbor-credentials',
                        usernameVariable: 'HARBOR_USER',
                        passwordVariable: 'HARBOR_PASSWORD'
                    )
                ]) {
                    sh '''
                        printf '%s' "$HARBOR_PASSWORD" | \
                            podman login ${HARBOR_REGISTRY} \
                            --username "$HARBOR_USER" \
                            --password-stdin

                        podman push \
                            ${HARBOR_REGISTRY}/${HARBOR_PROJECT}/${IMAGE_NAME}:${BUILD_NUMBER}
                    '''
                }
            }
        }

        stage('Update GitOps Repository') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'github-credentials',
                        usernameVariable: 'GITHUB_USER',
                        passwordVariable: 'GITHUB_TOKEN'
                    )
                ]) {
                    sh '''
                        rm -rf gitops

                        git clone \
                            https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/mattang-e/server-inventory-k8s.git \
                            gitops

                        cd gitops

                        sed -i \
                            "s|image: harbor.lab.local/server-inventory/server-inventory-api:.*|image: harbor.lab.local/server-inventory/server-inventory-api:${BUILD_NUMBER}|" \
                            api/deployment.yaml

                        git config user.name "jenkins"
                        git config user.email "jenkins@lab.local"

                        git add api/deployment.yaml
                        git commit -m "Update server-inventory-api image to ${BUILD_NUMBER}"

                        git push origin main
                    '''
                }
            }
        }
    }
}