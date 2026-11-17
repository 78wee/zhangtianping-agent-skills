import Foundation
import Vision
import AppKit

let args = CommandLine.arguments
if args.count < 3 {
    fputs("Usage: vision_ocr.swift output.txt image...\n", stderr)
    exit(2)
}

let outPath = args[1]
let imagePaths = Array(args.dropFirst(2))
var result = ""

let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.usesLanguageCorrection = true
if #available(macOS 12.0, *) {
    request.recognitionLanguages = ["zh-Hans", "en-US"]
}
if #available(macOS 13.0, *) {
    request.revision = VNRecognizeTextRequestRevision3
}

for imagePath in imagePaths {
    result += "\n===== \(URL(fileURLWithPath: imagePath).lastPathComponent) =====\n"
    guard let nsImage = NSImage(contentsOfFile: imagePath),
          let tiff = nsImage.tiffRepresentation,
          let bitmap = NSBitmapImageRep(data: tiff),
          let cgImage = bitmap.cgImage else {
        result += "[could not load image]\n"
        continue
    }

    let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
    do {
        try handler.perform([request])
        let observations = request.results ?? []
        let sorted = observations.sorted { a, b in
            let dy = abs(a.boundingBox.midY - b.boundingBox.midY)
            if dy > 0.012 { return a.boundingBox.midY > b.boundingBox.midY }
            return a.boundingBox.minX < b.boundingBox.minX
        }
        for obs in sorted {
            if let top = obs.topCandidates(1).first {
                let bb = obs.boundingBox
                result += String(format: "[%.3f %.3f %.3f %.3f] %@\n",
                                 bb.minX, bb.minY, bb.width, bb.height, top.string)
            }
        }
    } catch {
        result += "[ocr error: \(error)]\n"
    }
}

try result.write(toFile: outPath, atomically: true, encoding: .utf8)

