// This file is part of OpenCV project.
// It is subject to the license terms in the LICENSE file found in the top-level directory
// of this distribution and at http://opencv.org/license.html.

#include "precomp.hpp"

#include <opencv2/core/utils/configuration.private.hpp>
#include <opencv2/core/utils/logger.hpp>

#include <sstream>
#include <iostream>
#include <fstream>

#ifdef __ANDROID__
# include <android/log.h>
#endif

namespace cv {
namespace utils {
namespace logging {

static LogLevel parseLogLevelConfiguration()
{
    (void)getInitializationMutex();  // ensure initialization of global objects

    static cv::String param_log_level = utils::getConfigurationParameterString("OPENCV_LOG_LEVEL",
#if defined NDEBUG
            "WARNING"
#else
            "INFO"
#endif
    );
    if (param_log_level == "DISABLED" || param_log_level == "disabled" ||
        param_log_level == "0" || param_log_level == "OFF" || param_log_level == "off")
        return LOG_LEVEL_SILENT;
    if (param_log_level == "FATAL" || param_log_level == "fatal")
        return LOG_LEVEL_FATAL;
    if (param_log_level == "ERROR" || param_log_level == "error")
        return LOG_LEVEL_ERROR;
    if (param_log_level == "WARNING" || param_log_level == "warning" ||
        param_log_level == "WARNINGS" || param_log_level == "warnings" ||
        param_log_level == "WARN" || param_log_level == "warn")
        return LOG_LEVEL_WARNING;
    if (param_log_level == "INFO" || param_log_level == "info")
        return LOG_LEVEL_INFO;
    if (param_log_level == "DEBUG" || param_log_level == "debug")
        return LOG_LEVEL_DEBUG;
    if (param_log_level == "VERBOSE" || param_log_level == "verbose")
        return LOG_LEVEL_VERBOSE;
    std::cerr << "ERROR: Unexpected logging level value: " << param_log_level << std::endl;
    return LOG_LEVEL_INFO;
}

static LogLevel& getLogLevelVariable()
{
    static LogLevel g_logLevel = parseLogLevelConfiguration();
    return g_logLevel;
}

LogLevel setLogLevel(LogLevel logLevel)
{
    LogLevel old = getLogLevelVariable();
    getLogLevelVariable() = logLevel;
    return old;
}

LogLevel getLogLevel()
{
    return getLogLevelVariable();
}

namespace internal {

static int getShowTimestampMode()
{
    static bool param_timestamp_enable = utils::getConfigurationParameterBool("OPENCV_LOG_TIMESTAMP", true);
    static bool param_timestamp_ns_enable = utils::getConfigurationParameterBool("OPENCV_LOG_TIMESTAMP_NS", false);
    return (param_timestamp_enable ? 1 : 0) + (param_timestamp_ns_enable ? 2 : 0);
}

void writeLogMessage(LogLevel logLevel, const char* message)
{
    const int threadID = cv::utils::getThreadID();

    std::string message_id;
    switch (getShowTimestampMode())
    {
        case 1: message_id = cv::format("%d@%0.3f", threadID, getTimestampNS() * 1e-9); break;
        case 1+2: message_id = cv::format("%d@%llu", threadID, getTimestampNS()); break;
        default: message_id = cv::format("%d", threadID); break;
    }

    std::ostringstream ss;
    switch (logLevel)
    {
    case LOG_LEVEL_FATAL:   ss << "[FATAL:" << message_id << "] " << message << std::endl; break;
    case LOG_LEVEL_ERROR:   ss << "[ERROR:" << message_id << "] " << message << std::endl; break;
    case LOG_LEVEL_WARNING: ss << "[ WARN:" << message_id << "] " << message << std::endl; break;
    case LOG_LEVEL_INFO:    ss << "[ INFO:" << message_id << "] " << message << std::endl; break;
    case LOG_LEVEL_DEBUG:   ss << "[DEBUG:" << message_id << "] " << message << std::endl; break;
    case LOG_LEVEL_VERBOSE: ss << message << std::endl; break;
    case LOG_LEVEL_SILENT: return;  // avoid compiler warning about incomplete switch
    case ENUM_LOG_LEVEL_FORCE_INT: return;  // avoid compiler warning about incomplete switch
    }
#ifdef __ANDROID__
    int android_logLevel = ANDROID_LOG_INFO;
    switch (logLevel)
    {
    case LOG_LEVEL_FATAL:   android_logLevel = ANDROID_LOG_FATAL; break;
    case LOG_LEVEL_ERROR:   android_logLevel = ANDROID_LOG_ERROR; break;
    case LOG_LEVEL_WARNING: android_logLevel = ANDROID_LOG_WARN; break;
    case LOG_LEVEL_INFO:    android_logLevel = ANDROID_LOG_INFO; break;
    case LOG_LEVEL_DEBUG:   android_logLevel = ANDROID_LOG_DEBUG; break;
    case LOG_LEVEL_VERBOSE: android_logLevel = ANDROID_LOG_VERBOSE; break;
    default:
        break;
    }
    __android_log_print(android_logLevel, "OpenCV/" CV_VERSION, "%s", ss.str().c_str());
#endif
    std::ostream* out = (logLevel <= LOG_LEVEL_WARNING) ? &std::cerr : &std::cout;
    (*out) << ss.str();
    if (logLevel <= LOG_LEVEL_WARNING)
        (*out) << std::flush;
}

} // namespace

}}} // namespace
