pipeline {
    agent any
    options {
        timestamps()
        timeout(time:10, unit:'MINUTES')
        
        buildDiscarder (logRotator(
            numToKeepStr: '4',
            daysToKeepStr: '7',
            artifactNumToKeepStr: '30'))
    }
    environment {

            DOCKER_IMAGE_AWS = "644435390668.dkr.ecr.us-east-1.amazonaws.com/rotem-todo-app"
            LOGIN_ECR= "aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 644435390668.dkr.ecr.us-east-1.amazonaws.com"
    }

    stages {
            stage("BUILD APP + UNIT TEST"){
                when { expression { env.GIT_BRANCH != 'feature' }}
                steps{
                    script{
                        // withCredentials([usernamePassword(credentialsId: 'git_https_account', passwordVariable: 'password', usernameVariable: 'username')]) {
                        //     git url: 'https://github.com/RotemK1/todo-docker.git'
                                //app_todo = docker.build('rotem-todo-app')
                                sh "docker-compose up -d"
                                sh "timeout 60 wget --retry-connrefused --tries=60 --waitretry=2 -q rotem-todo-app:5000 -O /dev/null"
                          //      sh"docker run -d --name rotem-todo-app --network workspace rotem-todo-app"
                        }
                    }
                }
            }
        

        // stage('E2E'){
        //     when { expression { env.GIT_BRANCH == 'feature' }}
        //     steps{
        //         echo "#########################################"
        //         echo "                 E2E                     "
        //         echo "#########################################"
        //         script{
        //                 sh "docker-compose up -d"

        //                 // TO DO TESTING WITH POST, GET, DELETE.

        //         }
        //     }
        // }


        // stage('TAG & PUBLISH '){
        //     when { expression { env.GIT_BRANCH == 'master' }}
        //     steps{
        //         echo "#########################################"
        //         echo "           TAGGING AND PUBLISH          "
        //         echo "#########################################"

        //         script{
        //             withCredentials([[
        //                 $class: 'AmazonWebServicesCredentialsBinding',
        //                 credentialsId: "aws_account",
        //                 accessKeyVariable: 'AWS_ACCESS_KEY_ID',
        //                 secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
        //             ]]) {
        //                 sh "aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 644435390668.dkr.ecr.us-east-1.amazonaws.com"
        //                 docker.withRegistry("644435390668.dkr.ecr.us-east-1.amazonaws.com/rotem-todo-app", "ecr:eu-west-1:rotem_aws_credentials"){
        //                 app_toxic.push("${TAG}")}
        //                 }
        //             }
        //         }        
        //     }
        // }

        // stage("BUILD APP"){
        //     when { expression { env.GIT_BRANCH == 'master' }}
        //     steps{
        //         script{
        //             withCredentials([usernamePassword(credentialsId: 'git_https_account', passwordVariable: 'password', usernameVariable: 'username')]) {
        //                 git url: 'https://github.com/RotemK1/app-helm.git'
        //                 // sed and switch and helm with diffrent tag in values
        //             }
        //         }
        //     }
        // }     
    }    
  post {
    // always {

    //     emailext (
    //         to:      "rotem.devops.test@gmail.com",
    //         subject: "Jenkins - ${env.JOB_NAME}, build ${env.BUILD_DISPLAY_NAME} - ${currentBuild.currentResult}",
    //         body:    """
    //         <p>Jenkins job <a href='${env.JOB_URL}'>${env.JOB_NAME}</a> (<a href='${env.BUILD_URL}'>build ${env.BUILD_DISPLAY_NAME}</a>) has result <strong>${currentBuild.currentResult}</strong>!
    //         <br>You can view the <a href='${env.BUILD_URL}console'>console log here</a>.</p>
    //         <br><strong>terraform Workspaces list:</strong></p>
    //         ${TERRAFORM_WORKSPACE}</p>
    //         <br><strong>Deleted Workspace list:</strong></p>
    //         <br>${DELETED_WORKSPACE}</p>
    //         <p>Source code from commit: <a href='${env.GIT_URL}/commit/${env.GIT_COMMIT}'>${env.GIT_COMMIT}</a> (of branch <em>${env.GIT_BRANCH}</em>).</p>
    //         <p><img src='https://www.jenkins.io/images/logos/jenkins/jenkins.png' alt='jenkins logo' width='123' height='170'></p>
    //         """
    //     )
    // }
        failure {
            echo "i failed!"
        }              
        success {
            echo 'I succeeded!'
        }
    }
}
