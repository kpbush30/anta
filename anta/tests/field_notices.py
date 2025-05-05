# Copyright (c) 2023-2025 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
"""Module related to field notices tests."""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from anta.decorators import skip_on_platforms
from anta.models import AntaCommand, AntaTest

if TYPE_CHECKING:
    from anta.models import AntaTemplate


class VerifyFieldNotice99Resolution(AntaTest):
    """Verifies if the device is using an Aboot version that fixes the bug discussed in the Field Notice 99.

    Aboot manages system settings prior to EOS initialization.

    Reference: https://www.arista.com/en/support/advisories-notices/field-notice/21317-field-notice-0099

    Expected Results
    ----------------
    * Success: The test will pass if the device is using an Aboot version that fixes the bug discussed in the Field Notice 44.
    * Failure: The test will fail if the device is not using an Aboot version that fixes the bug discussed in the Field Notice 44.

    Examples
    --------
    ```yaml
    anta.tests.field_notices:
      - VerifyFieldNotice44Resolution:
    ```
    """

    description = "Verifies that the device is using the correct Aboot version per FN0099."
    categories: ClassVar[list[str]] = ["field notices"]
    commands: ClassVar[list[AntaCommand | AntaTemplate]] = [AntaCommand(command="show boot", revision=1), AntaCommand(command="show platform bios", revision=1)]

    @skip_on_platforms(["cEOSLab", "vEOS-lab", "cEOSCloudLab", "vEOS"])
    @AntaTest.anta_test
    def test(self) -> None:
        """Main test function for VerifyFieldNotice44Resolution."""

        boot_output = self.instance_commands[0].json_output
        platform_output = self.instance_commands[1].json_output

        affected_aboot_versions = [
            "6.1.11-18938843",
            "6.2.0-24152155",
            "6.2.0-24152155",
            "7.1.4-14169220",
            "7.1.5-20123938",
            "7.1.6-22971530",
            "9.0.1-11845100",
            "9.0.2-12970762",
            "9.0.3-14223577",
            "9.0.4-16346895",
            "10.0.1-22594906",
            "10.0.1-22771386",
        ]

        sb_supported = boot_output["securebootSupported"]
        sb_enabled = boot_output["securebootEnabled"]
        spi_protected = boot_output["spiFlashWriteProtected"]
        aboot_version = f"{platform_output["runningVersion"]["version"]}-{platform_output["runningVersion"]["changeNumber"]}"

        if not sb_supported:
            self.result.is_skipped("Device is not impacted by FN0099, secure boot not supported")
        
        elif not sb_enabled:
            self.result.is_success("Device is not impacted by FN0099, secure boot not enabled")
     
        elif sb_supported and sb_enabled:
            if aboot_version in affected_aboot_versions:
                self.result.is_failure(f"Device is running secure boot on an affected version of Aboot: {aboot_version}\n")

                if spi_protected:
                    self.result.is_failure(f"Device is running secure boot with SPI flash write protection enabled, see FN0099 for more details")
                
                self.result.is_failure(f"Device is running incorrect version of aboot {aboot_version}")

class VerifyFieldNotice44Resolution(AntaTest):
    """Verifies if the device is using an Aboot version that fixes the bug discussed in the Field Notice 44.

    Aboot manages system settings prior to EOS initialization.

    Reference: https://www.arista.com/en/support/advisories-notices/field-notice/8756-field-notice-44

    Expected Results
    ----------------
    * Success: The test will pass if the device is using an Aboot version that fixes the bug discussed in the Field Notice 44.
    * Failure: The test will fail if the device is not using an Aboot version that fixes the bug discussed in the Field Notice 44.

    Examples
    --------
    ```yaml
    anta.tests.field_notices:
      - VerifyFieldNotice44Resolution:
    ```
    """

    description = "Verifies that the device is using the correct Aboot version per FN0044."
    categories: ClassVar[list[str]] = ["field notices"]
    commands: ClassVar[list[AntaCommand | AntaTemplate]] = [AntaCommand(command="show version detail", revision=1)]

    @skip_on_platforms(["cEOSLab", "vEOS-lab", "cEOSCloudLab", "vEOS"])
    @AntaTest.anta_test
    def test(self) -> None:
        """Main test function for VerifyFieldNotice44Resolution."""
        command_output = self.instance_commands[0].json_output

        devices = [
            "DCS-7010T-48",
            "DCS-7010T-48-DC",
            "DCS-7050TX-48",
            "DCS-7050TX-64",
            "DCS-7050TX-72",
            "DCS-7050TX-72Q",
            "DCS-7050TX-96",
            "DCS-7050TX2-128",
            "DCS-7050SX-64",
            "DCS-7050SX-72",
            "DCS-7050SX-72Q",
            "DCS-7050SX2-72Q",
            "DCS-7050SX-96",
            "DCS-7050SX2-128",
            "DCS-7050QX-32S",
            "DCS-7050QX2-32S",
            "DCS-7050SX3-48YC12",
            "DCS-7050CX3-32S",
            "DCS-7060CX-32S",
            "DCS-7060CX2-32S",
            "DCS-7060SX2-48YC6",
            "DCS-7160-48YC6",
            "DCS-7160-48TC6",
            "DCS-7160-32CQ",
            "DCS-7280SE-64",
            "DCS-7280SE-68",
            "DCS-7280SE-72",
            "DCS-7150SC-24-CLD",
            "DCS-7150SC-64-CLD",
            "DCS-7020TR-48",
            "DCS-7020TRA-48",
            "DCS-7020SR-24C2",
            "DCS-7020SRG-24C2",
            "DCS-7280TR-48C6",
            "DCS-7280TRA-48C6",
            "DCS-7280SR-48C6",
            "DCS-7280SRA-48C6",
            "DCS-7280SRAM-48C6",
            "DCS-7280SR2K-48C6-M",
            "DCS-7280SR2-48YC6",
            "DCS-7280SR2A-48YC6",
            "DCS-7280SRM-40CX2",
            "DCS-7280QR-C36",
            "DCS-7280QRA-C36S",
        ]
        variants = ["-SSD-F", "-SSD-R", "-M-F", "-M-R", "-F", "-R"]

        model = command_output["modelName"]
        for variant in variants:
            model = model.replace(variant, "")
        if model not in devices:
            self.result.is_skipped("Device is not impacted by FN044")
            return

        for component in command_output["details"]["components"]:
            if component["name"] == "Aboot":
                aboot_version = component["version"].split("-")[2]
                break
        else:
            self.result.is_failure("Aboot component not found")
            return

        self.result.is_success()
        incorrect_aboot_version = (
            (aboot_version.startswith("4.0.") and int(aboot_version.split(".")[2]) < 7)
            or (aboot_version.startswith("4.1.") and int(aboot_version.split(".")[2]) < 1)
            or (
                (aboot_version.startswith("6.0.") and int(aboot_version.split(".")[2]) < 9)
                or (aboot_version.startswith("6.1.") and int(aboot_version.split(".")[2]) < 7)
            )
        )
        if incorrect_aboot_version:
            self.result.is_failure(f"Device is running incorrect version of aboot {aboot_version}")


class VerifyFieldNotice72Resolution(AntaTest):
    """Verifies if the device is potentially exposed to Field Notice 72, and if the issue has been mitigated.

    Reference: https://www.arista.com/en/support/advisories-notices/field-notice/17410-field-notice-0072

    Expected Results
    ----------------
    * Success: The test will pass if the device is not exposed to FN72 and the issue has been mitigated.
    * Failure: The test will fail if the device is exposed to FN72 and the issue has not been mitigated.

    Examples
    --------
    ```yaml
    anta.tests.field_notices:
      - VerifyFieldNotice72Resolution:
    ```
    """

    description = "Verifies if the device is exposed to FN0072, and if the issue has been mitigated."
    categories: ClassVar[list[str]] = ["field notices"]
    commands: ClassVar[list[AntaCommand | AntaTemplate]] = [AntaCommand(command="show version detail", revision=1)]

    @skip_on_platforms(["cEOSLab", "vEOS-lab", "cEOSCloudLab", "vEOS"])
    @AntaTest.anta_test
    def test(self) -> None:
        """Main test function for VerifyFieldNotice72Resolution."""
        command_output = self.instance_commands[0].json_output

        devices = ["DCS-7280SR3-48YC8", "DCS-7280SR3K-48YC8"]
        variants = ["-SSD-F", "-SSD-R", "-M-F", "-M-R", "-F", "-R"]
        model = command_output["modelName"]

        for variant in variants:
            model = model.replace(variant, "")
        if model not in devices:
            self.result.is_skipped("Platform is not impacted by FN072")
            return

        serial = command_output["serialNumber"]
        number = int(serial[3:7])

        if "JPE" not in serial and "JAS" not in serial:
            self.result.is_skipped("Device not exposed")
            return

        if model == "DCS-7280SR3-48YC8" and "JPE" in serial and number >= 2131:
            self.result.is_skipped("Device not exposed")
            return

        if model == "DCS-7280SR3-48YC8" and "JAS" in serial and number >= 2041:
            self.result.is_skipped("Device not exposed")
            return

        if model == "DCS-7280SR3K-48YC8" and "JPE" in serial and number >= 2134:
            self.result.is_skipped("Device not exposed")
            return

        if model == "DCS-7280SR3K-48YC8" and "JAS" in serial and number >= 2041:
            self.result.is_skipped("Device not exposed")
            return

        # Because each of the if checks above will return if taken, we only run the long check if we get this far
        for entry in command_output["details"]["components"]:
            if entry["name"] == "FixedSystemvrm1":
                if int(entry["version"]) < 7:
                    self.result.is_failure("Device is exposed to FN72")
                else:
                    self.result.is_success("FN72 is mitigated")
                return
        # We should never hit this point
        self.result.is_failure("Error in running test - Component FixedSystemvrm1 not found in 'show version'")
