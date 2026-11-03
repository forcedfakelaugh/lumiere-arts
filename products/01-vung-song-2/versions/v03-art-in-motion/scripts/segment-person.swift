import Foundation
import AVFoundation
import Vision
import CoreImage

// Frame-by-frame temporally stateful person matte, including hair and clothing.
// Input proxies must be upright 1080x1920, 30 fps.
let args = CommandLine.arguments
guard args.count == 6 else {
    fputs("Usage: segment-person input.mp4 start duration output.mp4 width\n", stderr)
    exit(1)
}
let input = URL(fileURLWithPath: args[1])
let start = Double(args[2])!, duration = Double(args[3])!
let width = Int(args[5])!, height = width * 16 / 9
let asset = AVURLAsset(url: input)
let reader = try AVAssetReader(asset: asset)
let track = asset.tracks(withMediaType: .video)[0]
let output = AVAssetReaderTrackOutput(track: track, outputSettings: [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA])
output.alwaysCopiesSampleData = false
reader.add(output)
reader.timeRange = CMTimeRange(start: CMTime(seconds: start, preferredTimescale: 30), duration: CMTime(seconds: duration, preferredTimescale: 30))
let request = VNGeneratePersonSegmentationRequest()
request.qualityLevel = .accurate
request.outputPixelFormat = kCVPixelFormatType_OneComponent8
let handler = VNSequenceRequestHandler()
let context = CIContext(options: [.cacheIntermediates: false])
let encoder = Process()
encoder.executableURL = URL(fileURLWithPath: "/opt/homebrew/bin/ffmpeg")
encoder.arguments = ["-y", "-v", "error", "-f", "rawvideo", "-pixel_format", "gray", "-video_size", "\(width)x\(height)", "-framerate", "30", "-i", "pipe:0", "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "12", "-pix_fmt", "yuv420p", "-movflags", "+faststart", args[4]]
let pipe = Pipe()
encoder.standardInput = pipe
try encoder.run()
reader.startReading()
var count = 0
let begun = Date()
while let sample = output.copyNextSampleBuffer() {
    try autoreleasepool {
        guard let pixels = CMSampleBufferGetImageBuffer(sample) else { return }
        try handler.perform([request], on: pixels, orientation: .up)
        guard let result = request.results?.first else { throw NSError(domain: "No person mask", code: 1) }
        let mask = CIImage(cvPixelBuffer: result.pixelBuffer)
        let resized = mask.transformed(by: CGAffineTransform(scaleX: CGFloat(width) / mask.extent.width, y: CGFloat(height) / mask.extent.height))
        var data = Data(count: width * height)
        data.withUnsafeMutableBytes { raw in
            context.render(resized, toBitmap: raw.baseAddress!, rowBytes: width, bounds: CGRect(x: 0, y: 0, width: width, height: height), format: .L8, colorSpace: CGColorSpaceCreateDeviceGray())
        }
        try pipe.fileHandleForWriting.write(contentsOf: data)
        count += 1
        if count % 30 == 0 { fputs("\(count) frames / \(String(format: "%.1f", Date().timeIntervalSince(begun)))s\n", stderr) }
    }
}
try pipe.fileHandleForWriting.close()
encoder.waitUntilExit()
guard reader.status == .completed && encoder.terminationStatus == 0 else {
    fputs("Reader/encoder failed: \(String(describing: reader.error))\n", stderr)
    exit(2)
}
guard count == Int((duration * 30).rounded()) else {
    fputs("Frame count mismatch: \(count)\n", stderr)
    exit(3)
}
print("Wrote \(count) frames to \(args[4])")
