import core from '@actions/core'
import github from '@actions/github'
import exec from '@actions/exec'
import fs from 'fs'
import path from 'path'

// function run() {
//     // 1) Get some input values
//     const bucket = core.getInput('bucket', {required: true})
//     const bucketRegion = core.getInput('bucket-region', {required: true})
//     const distFolder = core.getInput('dist-folder', {required: true})
//
//     // 2) Upload files
//     const s3Uri = `s3://${bucket}`
//     exec.exec(`aws s3 sync ${distFolder} ${s3Uri} --region ${bucketRegion}`)
//
//     const websiteUrl = `http://${bucket}.s3-website-${bucketRegion}.amazonaws.com`
//     core.setOutput('website-url', websiteUrl) // $GITHUB_OUTPUT(::set-output)
// }

async function run() {
    try {
        // 1) Get some input values
        const bucket = core.getInput('bucket', {required: true})
        const bucketRegion = core.getInput('bucket-region', {required: true})
        const distFolder = core.getInput('dist-folder', {required: true})

        // 2) Upload files with ContentType
        const s3Uri = `s3://${bucket}`
        const files = fs.readdirSync(distFolder)

        for (const file of files) {
            const filePath = path.join(distFolder, file)
            const contentType = 'text/html' // 원하는 ContentType 설정
            await exec.exec(`aws s3 cp ${filePath} ${s3Uri}/${file} --region ${bucketRegion} --content-type ${contentType}`)
        }

        // 3) Set website URL output
        const websiteUrl = `http://${bucket}.s3-website-${bucketRegion}.amazonaws.com`
        core.setOutput('website-url', websiteUrl) // $GITHUB_OUTPUT(::set-output)
    } catch (error) {
        core.setFailed(error.message)
    }
}

run()

run()
